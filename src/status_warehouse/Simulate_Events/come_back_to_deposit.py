from simpy import Environment

# from src.drawer import Drawer
from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse


class ComeBackToDeposit(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self):
        print(f"Time {self.env.now:5.2f} - Start come back to deposit position")
        yield self.env.process(self.get_warehouse().come_back_to_deposit(self.get_warehouse().get_drawer_of_support()))
        print(f"Time {self.env.now:5.2f} - ~ Finish ~")
