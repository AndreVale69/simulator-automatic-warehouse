from simpy import Environment
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.simulation import Floor


class TakeBay(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor: Floor):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self, drawer: Drawer):
        print("Test")
