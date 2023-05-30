from simpy import Environment

# from src.drawer import Drawer
from sim.simulation import Simulation
from sim.status_warehouse.Simulate_Events.action import Action
from sim.warehouse import Warehouse


class Buffer(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self):
        # try to take buffer resource
        with self.get_simulation().get_res_buffer().request() as req_buf:
            yield req_buf
            # try to take deposit resource
            with self.get_simulation().get_res_deposit().request() as req_dep:
                yield req_dep
                # check if the deposit and the buffer are empty and full iff the resources are taken
                if self.get_warehouse().get_carousel().is_buffer_full() and \
                        not self.get_warehouse().get_carousel().is_deposit_full():
                    print(f"Time {self.env.now:5.2f} - Start loading buffer drawer inside the deposit")
                    yield self.env.process(self.get_warehouse().loading_buffer_and_remove())
                    print(f"Time {self.env.now:5.2f} - Finish loading buffer drawer inside the deposit")
