from logging import getLogger
from datetime import datetime, timedelta
from simpy import Environment

from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.buffer import Buffer
from src.sim.simulation.actions.move.go_to_buffer import GoToBuffer
from src.sim.simulation.actions.move.go_to_deposit import GoToDeposit
from src.sim.simulation.actions.move.move import Move
from src.sim.simulation.actions.move.unload import Unload
from src.sim.simulation.actions.move.vertical import Vertical
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse  # , Drawer

logger = getLogger(__name__)


class ExtractDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, destination):
        """
        The extract of a drawer (ExtractDrawer action) is the movement from a column to the deposit (bay).

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        """
        super().__init__(env, warehouse, simulation, destination)

    def simulate_action(self):
        start_time = datetime.now() + timedelta(seconds=self.env.now)

        # try to release the drawer in the deposit
        if not self.warehouse.get_carousel().is_deposit_full():
            with self.simulation.get_res_deposit().request() as req:
                yield req
                yield self.env.process(self.actions(load_in_buffer=False))
        else:
            # if the deposit is under process by another one, release it inside the buffer
            with self.simulation.get_res_buffer().request() as req:
                yield req
                yield self.env.process(self.actions(load_in_buffer=True))
            # exec Buffer process
            wait_buff = self.env.process(Buffer(self.env, self.warehouse, self.simulation).simulate_action())
            # check GoToDeposit move
            yield self.env.process(super().simulate_action())
            # wait the buffer process
            yield wait_buff

        end_time = datetime.now() + timedelta(seconds=self.env.now)

        yield self.simulation.get_store_history().put({
            'Type of Action': ActionEnum.EXTRACT_DRAWER.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })

    def actions(self, load_in_buffer: bool):
        """
        Perform the real action.
        If the deposit is full, load_in_buffer should be True.

        :type load_in_buffer: bool
        :param load_in_buffer: True to send the drawer inside the buffer, False to send the drawer in the bay.
        """
        # choice a random drawer
        self.set_drawer(self.warehouse.choice_random_drawer())
        # move the floor
        yield self.env.process(Vertical(self.env, self.warehouse, self.simulation, self.drawer,
                                        self.destination).simulate_action())
        # unloading drawer
        yield self.env.process(Unload(self.env, self.warehouse, self.simulation, self.drawer,
                                      self.destination).simulate_action())
        # come back to the deposit
        if load_in_buffer:
            yield self.env.process(GoToBuffer(self.env, self.warehouse, self.simulation,
                                              self.drawer, self.destination).simulate_action())
        else:
            yield self.env.process(GoToDeposit(self.env, self.warehouse, self.simulation,
                                               self.drawer, self.destination).simulate_action())
        logger.debug(f"Time {self.env.now:5.2f} - Start to load in the carousel")
        yield self.env.process(self.simulation.load_in_carousel(self.drawer, self.destination, load_in_buffer))
