import datetime

from simpy import Environment

from src.sim.simulation import Simulation
from src.sim.status_warehouse.simulate_events.move.load import Load
from src.sim.status_warehouse.simulate_events.move.move import Move
from src.sim.status_warehouse.simulate_events.move.unload import Unload
from src.sim.status_warehouse.simulate_events.move.vertical import Vertical
from src.sim.status_warehouse.simulate_events.buffer import Buffer
from src.sim.warehouse import Warehouse
from src.sim.status_warehouse.simulate_events.action_enum import ActionEnum


class SendBackDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, destination):
        super().__init__(env, warehouse, simulation, destination)

    def simulate_action(self):
        start_time = datetime.datetime.now() + datetime.timedelta(seconds=self.get_env().now)

        with self.get_simulation().get_res_deposit().request() as req:
            # try to take the drawer inside the deposit
            yield req
            # set the drawer
            self.set_drawer(self.get_warehouse().get_carousel().get_deposit_entry().get_drawer())
            # unloading drawer
            yield self.env.process(
                Unload(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                       self.get_destination()).simulate_action())

        # exec Buffer process
        wait_buff = self.env.process(Buffer(self.get_env(), self.get_warehouse(), self.get_simulation()).simulate_action())

        # move the floor
        yield self.env.process(Vertical(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                        self.get_destination()).simulate_action())
        # loading drawer
        yield self.env.process(Load(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                    self.get_destination()).simulate_action())

        # check GoToDeposit move
        yield self.env.process(super().simulate_action())
        # wait the buffer process
        yield wait_buff

        end_time = datetime.datetime.now() + datetime.timedelta(seconds=self.get_env().now)

        yield self.simulation.get_store_history().put({
            'Type of Action': ActionEnum.SEND_BACK_DRAWER.value,
            'Start'         : start_time,
            'Finish'        : end_time
        })
