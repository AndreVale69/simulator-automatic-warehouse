from datetime import datetime, timedelta
from logging import getLogger

from simpy import Environment

from automatic_warehouse.simulation.actions.action_enum import ActionEnum
from automatic_warehouse.simulation.actions.move.go_to_bay import GoToBay
from automatic_warehouse.simulation.actions.move.load import Load
from automatic_warehouse.simulation.actions.move.move import Move
from automatic_warehouse.simulation.actions.move.unload import Unload
from automatic_warehouse.simulation.actions.move.vertical import Vertical
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse

logger = getLogger(__name__)


class SendBackTray(Move):
    """
    The send-back of a tray (SendBackTray action)
    is the movement of a tray from the bay to one of the columns.

    :type env: Environment
    :type warehouse: Warehouse
    :type simulation: Simulation
    :param env: the simulation environment (SimPy Environment).
    :param warehouse: the warehouse where the action is performed.
    :param simulation: the simulation where the action is performed.
    """

    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)
        self._go_to_bay: GoToBay = GoToBay(env, warehouse, simulation)
        self._unload: Unload = Unload(env, warehouse, simulation)
        self._vertical: Vertical = Vertical(env, warehouse, simulation)
        self._load: Load = Load(env, warehouse, simulation)

    def simulate_action(self, tray=None, destination=None):
        assert tray is None, logger.warning("The default action is to remove the tray from the bay, "
                                              "so the tray parameter is not taken into account.")
        simulation, warehouse, env = self.simulation, self.warehouse, self.env
        carousel = warehouse.get_carousel()

        start_time = datetime.now() + timedelta(seconds=env.now)

        with simulation.get_res_bay().request() as req:
            # try to take the tray inside the bay
            yield req
            # set the tray
            tray = carousel.get_bay_tray()
            # unloading tray
            yield env.process(self._unload.simulate_action(tray, destination))

        # exec Buffer process
        wait_buff = env.process(self.get_buffer().simulate_action())

        # move the floor
        yield env.process(self._vertical.simulate_action(tray, destination))
        # loading tray
        yield env.process(self._load.simulate_action(tray, destination))

        # check GoToBay move
        if carousel.is_bay_full():
            yield env.process(self._go_to_bay.simulate_action())

        # wait the buffer process
        yield wait_buff

        end_time = datetime.now() + timedelta(seconds=env.now)

        yield simulation.get_store_history().put({
            'Type of Action': ActionEnum.SEND_BACK_TRAY.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })
