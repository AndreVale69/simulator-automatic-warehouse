from datetime import datetime, timedelta
from logging import getLogger

from simpy import Environment

from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.move.go_to_deposit import GoToDeposit
from src.sim.simulation.actions.move.load import Load
from src.sim.simulation.actions.move.move import Move
from src.sim.simulation.actions.move.unload import Unload
from src.sim.simulation.actions.move.vertical import Vertical
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse

logger = getLogger(__name__)


class SendBackDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        """
        The send-back of a drawer (SendBackDrawer action)
        is the movement of a drawer from the bay to one of the columns.

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation)
        self._go_to_deposit: GoToDeposit = GoToDeposit(env, warehouse, simulation)
        self._unload: Unload = Unload(env, warehouse, simulation)
        self._vertical: Vertical = Vertical(env, warehouse, simulation)
        self._load: Load = Load(env, warehouse, simulation)

    def simulate_action(self, drawer=None, destination=None):
        assert drawer is None, logger.warning("The default action is to remove the drawer from the bay, "
                                              "so the drawer parameter is not taken into account.")
        simulation, warehouse, env = self.simulation, self.warehouse, self.env
        carousel = warehouse.get_carousel()

        start_time = datetime.now() + timedelta(seconds=env.now)

        with simulation.get_res_deposit().request() as req:
            # try to take the drawer inside the deposit
            yield req
            # set the drawer
            drawer = carousel.get_deposit_drawer()
            # unloading drawer
            yield env.process(self._unload.simulate_action(drawer, destination))

        # exec Buffer process
        wait_buff = env.process(self.get_buffer().simulate_action())

        # move the floor
        yield env.process(self._vertical.simulate_action(drawer, destination))
        # loading drawer
        yield env.process(self._load.simulate_action(drawer, destination))

        # check GoToDeposit move
        if carousel.is_deposit_full():
            yield env.process(self._go_to_deposit.simulate_action())

        # wait the buffer process
        yield wait_buff

        end_time = datetime.now() + timedelta(seconds=env.now)

        yield simulation.get_store_history().put({
            'Type of Action': ActionEnum.SEND_BACK_DRAWER.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })
