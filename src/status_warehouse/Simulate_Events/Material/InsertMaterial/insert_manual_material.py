from simpy import Environment

from src.drawer import Drawer
from src.material import Material
from src.simulation import Simulation
from status_warehouse.Simulate_Events.Material.InsertMaterial.insert_material import InsertMaterial
from src.warehouse import Warehouse


class InsertManualMaterial(InsertMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation,
                 duration: int, materials: list[Material]):
        super().__init__(env, warehouse, simulation, duration)
        self.materials = materials.copy()

    def get_materials(self) -> list[Material]:
        return self.materials

    # override
    def simulate_action(self):
        with self.get_simulation().get_res().request() as req:
            yield req
            print(f"Time {self.env.now:5.2f} - Start putting materials inside a drawer")
            # take the drawer that is outside
            drawer_output: Drawer = self.get_warehouse().get_carousel().get_deposit_entry().get_drawer()
            for material in self.get_materials():
                # add the material
                drawer_output.add_material(material)
            # estimate a time of the action
            yield self.env.timeout(self.get_duration())
