from datetime import datetime, timedelta
from logging import getLogger

from simpy import Environment

from automatic_warehouse.simulation.actions.action_enum import ActionEnum
from automatic_warehouse.simulation.actions.move.go_to_bay import GoToBay
from automatic_warehouse.simulation.actions.move.go_to_buffer import GoToBuffer
from automatic_warehouse.simulation.actions.move.move import Move
from automatic_warehouse.simulation.actions.move.unload import Unload
from automatic_warehouse.simulation.actions.move.vertical import Vertical
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse

logger = getLogger(__name__)


class ExtractTray(Move):
    """
    The extract of a tray (ExtractTray action) is the movement from a column to the bay.

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
        self._go_to_buffer: GoToBuffer = GoToBuffer(env, warehouse, simulation)
        self._unload: Unload = Unload(env, warehouse, simulation)
        self._vertical: Vertical = Vertical(env, warehouse, simulation)

    def simulate_action(self, tray=None, destination=None):
        assert tray is None, logger.warning("The default action is to select a random tray from the warehouse, "
                                              "so the tray parameter is not taken into account.")
        assert destination is not None, logger.error("The destination cannot be None!")
        simulation, warehouse, env = self.simulation, self.warehouse, self.env
        carousel = warehouse.get_carousel()

        start_time = datetime.now() + timedelta(seconds=env.now)

        # try to release the tray in the bay
        if not carousel.is_bay_full():
            with simulation.get_res_bay().request() as req:
                yield req
                yield env.process(self._actions(destination, False))
        else:
            # if the bay is under process by another one, release it inside the buffer
            with simulation.get_res_buffer().request() as req:
                yield req
                yield env.process(self._actions(destination, True))
            # exec Buffer process
            wait_buff = env.process(self.get_buffer().simulate_action())
            # check GoToBay move
            if carousel.is_bay_full():
                yield env.process(self._go_to_bay.simulate_action())
            # wait the buffer process
            yield wait_buff

        end_time = datetime.now() + timedelta(seconds=env.now)

        yield simulation.get_store_history().put({
            'Type of Action': ActionEnum.EXTRACT_TRAY.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })

    def _actions(self, destination, load_in_buffer: bool):
        """
        Perform the real action.
        If the bay is full, load_in_buffer should be True.

        :type destination: EnumContainer
        :type load_in_buffer: bool
        :param destination: the destination.
        :param load_in_buffer: True to send the tray inside the buffer, False to send the tray in the bay.
        """
        simulation, warehouse, env = self.simulation, self.warehouse, self.env

        # choice a random tray
        tray = warehouse.choice_random_tray()
        # move the floor
        yield env.process(self._vertical.simulate_action(tray, destination))
        # unloading tray
        yield env.process(self._unload.simulate_action(tray, destination))
        # come back to the bay
        yield env.process(
            self._go_to_buffer.simulate_action() if load_in_buffer else self._go_to_bay.simulate_action()
        )
        logger.debug(f"Time {env.now:5.2f} - Start to load in the carousel")
        yield env.process(simulation.load_in_carousel(tray, destination, load_in_buffer))
