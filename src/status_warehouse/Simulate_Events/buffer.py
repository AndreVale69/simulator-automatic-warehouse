from simpy import Environment

# from src.drawer import Drawer
from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse


class Buffer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self):
        while True:
            # wait until the communication channel is empty
            msg = yield self.get_simulation().get_comm_chan().get()
            # print(msg)
            # TODO: nuova variabile di aiuto che gestisca il problema di a
            print(f"Time {self.env.now:5.2f} - Start loading buffer drawer inside the deposit")
            yield self.env.process(self.get_warehouse().loading_buffer_and_remove())
            print(f"Time {self.env.now:5.2f} - Finish loading buffer drawer inside the deposit")
