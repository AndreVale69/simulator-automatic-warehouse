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

        with self.get_simulation().get_res_deposit().request() as req:
            yield req
            drawer_output = super().simulate_action()
            # generate random material
            mat_to_put = gen_rand_material()
            # add the material
            drawer_output.add_material(mat_to_put)
            # estimate a time of the action
            yield self.env.timeout(self.get_duration())