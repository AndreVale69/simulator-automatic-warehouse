from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.come_back_to_deposit import ComeBackToDeposit
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.status_warehouse.Simulate_Events.Move.unload import Unload
from src.status_warehouse.Simulate_Events.Move.vertical import Vertical
from src.warehouse import Warehouse, Drawer


class ExtractDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination: str):
        super().__init__(env, warehouse, simulation, drawer, destination)

    def simulate_action(self):
        # move the floor
        yield self.env.process(Vertical(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                        self.get_destination()).simulate_action())
        # unloading drawer
        yield self.env.process(Unload(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                      self.get_destination()).simulate_action())
        # come back to the deposit
        yield self.env.process(ComeBackToDeposit(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                                 self.get_drawer(), self.get_destination()).simulate_action())
        # show the drawer
        with self.get_simulation().get_res().request() as req:
            yield req
            print(f"Time {self.env.now:5.2f} - Start to load in the carousel")
            yield self.env.process(self.get_warehouse().load_in_carousel(self.get_drawer(), self.get_destination()))
        # force to come back to deposit
        yield self.env.process(ComeBackToDeposit(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                                 self.get_drawer(), self.get_destination()).simulate_action())
