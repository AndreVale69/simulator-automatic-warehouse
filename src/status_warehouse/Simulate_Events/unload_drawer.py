from simpy import Environment

from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
# from src.drawer import Drawer
from src.simulation import Simulation


class UnloadDrawer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self):
        print(f"Time {self.env.now:5.2f} - Start unloading a drawer")
        # unloading drawer
        yield self.env.process(self.get_warehouse().unload(self.get_warehouse().get_drawer_of_support()))
        # remove only from container
        self.get_warehouse().get_carousel().remove_drawer(self.get_warehouse().get_drawer_of_support())
        # trigger buffer.py process
        self.get_simulation().get_comm_chan().put("Check the buffer...")
