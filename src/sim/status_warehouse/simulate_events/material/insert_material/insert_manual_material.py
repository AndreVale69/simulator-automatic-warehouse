from simpy import Environment

# from src.drawer import Drawer
from sim.material import Material
from sim.simulation import Simulation
from sim.status_warehouse.simulate_events.material.insert_material.insert_material import InsertMaterial
from sim.warehouse import Warehouse


class InsertManualMaterial(InsertMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation,
                 duration: int, materials: list[Material]):
        super().__init__(env, warehouse, simulation, duration)
        self.materials = materials.copy()

    def get_materials(self) -> list[Material]:
        return self.materials

    # override
    def simulate_action(self):
        with self.get_simulation().get_res_deposit().request() as req:
            yield req
            drawer_output = super().simulate_action()
            for material in self.get_materials():
                # add the material
                drawer_output.add_material(material)
            # estimate a time of the action
            yield self.env.timeout(self.get_duration())
