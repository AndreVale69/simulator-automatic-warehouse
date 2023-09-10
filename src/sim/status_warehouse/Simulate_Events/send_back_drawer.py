from simpy import Environment

from sim.simulation import Simulation
from sim.status_warehouse.Simulate_Events.Move.load import Load
from sim.status_warehouse.Simulate_Events.Move.move import Move
from sim.status_warehouse.Simulate_Events.Move.unload import Unload
from sim.status_warehouse.Simulate_Events.Move.vertical import Vertical
from sim.status_warehouse.Simulate_Events.buffer import Buffer
from sim.warehouse import Warehouse


class SendBackDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, destination):
        super().__init__(env, warehouse, simulation, destination)

    def simulate_action(self):
        start_time = self.get_env().now

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

        end_time = self.get_env().now

        yield self.simulation.get_store_history().put(dict(Action="SendBackDrawer",
                                                           Start=str(start_time),
                                                           Finish=str(end_time)))
