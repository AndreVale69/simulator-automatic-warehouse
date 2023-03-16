from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.come_back_to_deposit import ComeBackToDeposit
from src.status_warehouse.Simulate_Events.Move.load import Load
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.status_warehouse.Simulate_Events.Move.unload import Unload
from src.status_warehouse.Simulate_Events.Move.vertical import Vertical
from src.status_warehouse.Simulate_Events.buffer import Buffer
from src.warehouse import Warehouse, Drawer


class SendBackDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, destination):
        super().__init__(env, warehouse, simulation, destination)

    def simulate_action(self):
        with self.get_simulation().get_res_deposit().request() as req:
            # try to take the drawer inside the deposit
            yield req
            # set the drawer
            import src
            src.warehouse.save_config(self.get_warehouse())
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
        # check ComeBackToDeposit move
        super().simulate_action()

        yield wait_buff
