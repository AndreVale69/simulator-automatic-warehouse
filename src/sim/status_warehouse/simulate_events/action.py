from abc import abstractmethod

from simpy import Environment

# from src.simulation import Floor
from sim.warehouse import Warehouse


class Action:
    def __init__(self, env: Environment, warehouse: Warehouse, simulation):
        self.env = env
        self.warehouse = warehouse
        self.simulation = simulation

    def get_env(self):
        return self.env

    def get_warehouse(self):
        return self.warehouse

    def get_simulation(self):
        return self.simulation

    @abstractmethod
    def simulate_action(self):
        pass
