from simpy import Environment

from src.simulation import Simulation
from src.warehouse import Warehouse


class LoadDrawer(object):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        self.env = env
        self.warehouse = warehouse
        self.simulation = simulation

    def get_env(self):
        return self.env

    def get_warehouse(self):
        return self.warehouse

    def get_simulation(self):
        return self.simulation

    def simulate_action(self):
        # add the drawer
        print(f"Time {self.env.now:5.2f} - Start loading a drawer")
        yield self.env.process(self.get_warehouse().load(self.get_warehouse().get_drawer_of_support()))
