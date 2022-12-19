from simpy import Environment
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.simulation import Floor


class ShowBuffer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor: Floor):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self, drawer: Drawer = None):
        while True:
            # DEBUG:
            # print(f"Time {self.env.now:5.2f} - Check the buffer...")

            # check if the buffer is to load or not
            if self.get_warehouse().check_buffer():
                print(f"Time {self.env.now:5.2f} - Start loading buffer drawer inside the deposit")
                yield self.env.process(self.get_warehouse().loading_buffer_and_remove())
            else:
                # DEBUG:
                # print(f"Time {self.env.now:5.2f} - No item! Go to sleep :)")
                yield self.env.timeout(2)
