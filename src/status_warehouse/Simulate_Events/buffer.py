from simpy import Environment
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.simulation import Simulation


class Buffer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor: Simulation):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self):
        from src.simulation import Simulation
        while True:
            # DEBUG:
            # print(f"Time {self.env.now:5.2f} - Check the buffer...")
            # check if the buffer is to load or not
            if self.get_warehouse().check_buffer() and not self.get_warehouse().check_deposit():
                print(f"Time {self.env.now:5.2f} - Start loading buffer drawer inside the deposit")
                yield self.env.process(self.get_warehouse().loading_buffer_and_remove())
            else:
                # DEBUG:
                # print(f"Time {self.env.now:5.2f} - No item! Go to sleep :)")
                yield self.env.timeout(0.001)
