from simpy import Environment
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.simulation import Floor


class UnloadDrawer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor: Floor):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self, drawer: Drawer):
        print(f"Time {self.env.now:5.2f} - Start unloading a drawer")
        # unloading drawer
        yield self.env.process(self.get_warehouse().unload(drawer))
        # remove only from container
        self.get_warehouse().get_carousel().remove_drawer(drawer)
