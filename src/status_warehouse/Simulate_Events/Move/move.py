from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.go_to_deposit_drawer import GoToDepositDrawer
from src.status_warehouse.Simulate_Events.Move.load_drawer import LoadDrawer
from src.status_warehouse.Simulate_Events.Move.unload_drawer import UnloadDrawer
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse


class Move(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)
        self.unload_drawer = UnloadDrawer(self.get_env(), self.get_warehouse(), self.get_simulation())
        self.go_to_deposit_drawer = GoToDepositDrawer(self.get_env(), self.get_warehouse(), self.get_simulation())
        self.load_drawer = LoadDrawer(self.get_env(), self.get_warehouse(), self.get_simulation())

    def get_unload_drawer(self):
        return self.unload_drawer

    def get_go_to_deposit_drawer(self):
        return self.go_to_deposit_drawer

    def get_load_drawer(self):
        return self.load_drawer

    def simulate_action(self):
        yield self.env.process(self.start_unload_drawer())
        yield self.env.process(self.start_go_to_deposit_drawer())
        yield self.env.process(self.start_load_drawer())

    def start_unload_drawer(self):
        yield self.env.process(self.get_unload_drawer().simulate_action())

    def start_go_to_deposit_drawer(self):
        yield self.env.process(self.get_go_to_deposit_drawer().simulate_action())

    def start_load_drawer(self):
        yield self.env.process(self.get_load_drawer().simulate_action())
