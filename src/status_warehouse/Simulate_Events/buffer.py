from simpy import Environment

from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
# from src.drawer import Drawer
from src.simulation import Simulation


class Buffer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self):
        while True:
            # wait until the communication channel is empty
            msg = yield self.get_simulation().get_comm_chan().get()
            print(msg)
            # check the buffer and the deposit
            if self.get_warehouse().check_buffer() and not self.get_warehouse().check_deposit():
                print(f"Time {self.env.now:5.2f} - Start loading buffer drawer inside the deposit")
                yield self.env.process(self.get_warehouse().loading_buffer_and_remove())
