from simpy import Environment

from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
# from src.drawer import Drawer
from src.simulation import Simulation


class LoadDrawer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor: Simulation):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self):
        # add the drawer
        print(f"Time {self.env.now:5.2f} - Start loading a drawer")
        yield self.env.process(self.get_warehouse().load(self.get_warehouse().get_drawer_of_support()))
