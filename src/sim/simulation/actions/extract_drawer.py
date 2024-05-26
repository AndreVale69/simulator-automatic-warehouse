from datetime import datetime, timedelta
from logging import getLogger

from simpy import Environment

from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.move.go_to_buffer import GoToBuffer
from src.sim.simulation.actions.move.go_to_deposit import GoToDeposit
from src.sim.simulation.actions.move.move import Move
from src.sim.simulation.actions.move.unload import Unload
from src.sim.simulation.actions.move.vertical import Vertical
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse

logger = getLogger(__name__)


class ExtractDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        """
        The extract of a drawer (ExtractDrawer action) is the movement from a column to the deposit (bay).

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation)
        self._go_to_deposit: GoToDeposit = GoToDeposit(env, warehouse, simulation)
        self._go_to_buffer: GoToBuffer = GoToBuffer(env, warehouse, simulation)
        self._unload: Unload = Unload(env, warehouse, simulation)
        self._vertical: Vertical = Vertical(env, warehouse, simulation)

    def simulate_action(self, drawer=None, destination=None):
        assert drawer is None, logger.warning("The default action is to select a random drawer from the warehouse, "
                                              "so the drawer parameter is not taken into account.")
        assert destination is not None, logger.error("The destination cannot be None!")
        simulation, warehouse, env = self.simulation, self.warehouse, self.env
        carousel = warehouse.get_carousel()

        start_time = datetime.now() + timedelta(seconds=env.now)

        # try to release the drawer in the deposit
        if not carousel.is_deposit_full():
            with simulation.get_res_deposit().request() as req:
                yield req
                yield env.process(self._actions(destination, False))
        else:
            # if the deposit is under process by another one, release it inside the buffer
            with simulation.get_res_buffer().request() as req:
                yield req
                yield env.process(self._actions(destination, True))
            # exec Buffer process
            wait_buff = env.process(self.get_buffer().simulate_action())
            # check GoToDeposit move
            if carousel.is_deposit_full():
                yield env.process(self._go_to_deposit.simulate_action())
            # wait the buffer process
            yield wait_buff

        end_time = datetime.now() + timedelta(seconds=env.now)

        yield simulation.get_store_history().put({
            'Type of Action': ActionEnum.EXTRACT_DRAWER.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })

    def _actions(self, destination, load_in_buffer: bool):
        """
        Perform the real action.
        If the deposit is full, load_in_buffer should be True.

        :type destination: EnumWarehouse
        :type load_in_buffer: bool
        :param destination: the destination.
        :param load_in_buffer: True to send the drawer inside the buffer, False to send the drawer in the bay.
        """
        simulation, warehouse, env = self.simulation, self.warehouse, self.env

        # choice a random drawer
        drawer = warehouse.choice_random_drawer()
        # move the floor
        yield env.process(self._vertical.simulate_action(drawer, destination))
        # unloading drawer
        yield env.process(self._unload.simulate_action(drawer, destination))
        # come back to the deposit
        yield env.process(
            self._go_to_buffer.simulate_action() if load_in_buffer else self._go_to_deposit.simulate_action()
        )
        logger.debug(f"Time {env.now:5.2f} - Start to load in the carousel")
        yield env.process(simulation.load_in_carousel(drawer, destination, load_in_buffer))
