from simpy import Environment

from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
# from src.drawer import Drawer
from src.simulation import Simulation


class GoToDepositDrawer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor: Simulation):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self):
        # move the floor
        print(f"Time {self.env.now:5.2f} - Start vertical move")
        yield self.env.process(self.get_warehouse().allocate_best_pos(self.get_warehouse().get_drawer_of_support()))
