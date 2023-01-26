import random

from simpy import Environment

from src.drawer import Drawer
from src.simulation import Simulation
from status_warehouse.Simulate_Events.Material.InsertMaterial.insert_material import InsertMaterial
from src.warehouse import Warehouse


class InsertRandomMaterial(InsertMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        super().__init__(env, warehouse, simulation, duration)

    # override
    def simulate_action(self):
        from src.material import gen_rand_material

        with self.get_simulation().get_semaphore_carousel().request() as req:
            yield req
            print(f"Time {self.env.now:5.2f} - Start putting materials inside a drawer")
            # take the drawer that is outside
            drawer_output: Drawer = self.get_warehouse().get_carousel().get_deposit_entry().get_drawer()
            # choice random material
            mat_to_rmv = random.choice(drawer_output.get_items())
            # remove the material
            drawer_output.remove_material(mat_to_rmv)
            # estimate a time of the action
            yield self.env.timeout(self.get_duration())
