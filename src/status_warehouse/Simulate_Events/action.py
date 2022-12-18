from abc import abstractmethod
from simpy import Environment
# from src.simulation import Floor
from src.warehouse import Warehouse
from src.drawer import Drawer


class Action:
    def __init__(self, env: Environment, warehouse: Warehouse, floor):
        self.env = env
        self.warehouse = warehouse
        self.floor = floor

    def get_env(self):
        return self.env

    def get_warehouse(self):
        return self.warehouse

    def get_floor(self):
        return self.floor

    @abstractmethod
    def simulate_action(self, drawer: Drawer):
        pass
