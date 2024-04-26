import datetime
import logging

from simpy import Environment

from src.sim.simulation import Simulation
from src.sim.status_warehouse.simulate_events.action_enum import ActionEnum
from src.sim.status_warehouse.simulate_events.buffer import Buffer
from src.sim.status_warehouse.simulate_events.move.go_to_buffer import GoToBuffer
from src.sim.status_warehouse.simulate_events.move.go_to_deposit import GoToDeposit
from src.sim.status_warehouse.simulate_events.move.move import Move
from src.sim.status_warehouse.simulate_events.move.unload import Unload
from src.sim.status_warehouse.simulate_events.move.vertical import Vertical
from src.sim.warehouse import Warehouse  # , Drawer

logger = logging.getLogger(__name__)


class ExtractDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, destination):
        super().__init__(env, warehouse, simulation, destination)

    def simulate_action(self):
        start_time = datetime.datetime.now() + datetime.timedelta(seconds=self.get_env().now)

        # try to release the drawer in the deposit
        if not self.get_warehouse().get_carousel().is_deposit_full():
            with self.get_simulation().get_res_deposit().request() as req:
                yield req
                yield self.env.process(self.actions(load_in_buffer=False))
        else:
            # if the deposit is under process by another one, release it inside the buffer
            with self.get_simulation().get_res_buffer().request() as req:
                yield req
                yield self.env.process(self.actions(load_in_buffer=True))
            # exec Buffer process
            wait_buff = self.env.process(Buffer(self.get_env(), self.get_warehouse(),
                                                self.get_simulation()).simulate_action())
            # check GoToDeposit move
            yield self.env.process(super().simulate_action())
            # wait the buffer process
            yield wait_buff

        end_time = datetime.datetime.now() + datetime.timedelta(seconds=self.get_env().now)

        yield self.simulation.get_store_history().put({
            'Type of Action': ActionEnum.EXTRACT_DRAWER.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })

    def actions(self, load_in_buffer: bool):
        # choice a random drawer
        self.set_drawer(self.get_warehouse().choice_random_drawer())
        # move the floor
        yield self.env.process(Vertical(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                        self.get_destination()).simulate_action())
        # unloading drawer
        yield self.env.process(Unload(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                      self.get_destination()).simulate_action())
        # come back to the deposit
        if load_in_buffer:
            yield self.env.process(GoToBuffer(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                              self.get_drawer(), self.get_destination()).simulate_action())
        else:
            yield self.env.process(GoToDeposit(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                               self.get_drawer(), self.get_destination()).simulate_action())
        logger.debug(f"Time {self.env.now:5.2f} - Start to load in the carousel")
        yield self.env.process(self.get_warehouse().load_in_carousel(self.get_drawer(), self.get_destination(),
                                                                     load_in_buffer=load_in_buffer))
