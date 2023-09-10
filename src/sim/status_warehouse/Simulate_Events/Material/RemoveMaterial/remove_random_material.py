import random

from simpy import Environment

# from src.drawer import Drawer
from sim.simulation import Simulation
from sim.status_warehouse.Simulate_Events.Material.RemoveMaterial.remove_material import RemoveMaterial
from sim.warehouse import Warehouse


class RemoveRandomMaterial(RemoveMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        super().__init__(env, warehouse, simulation, duration)

    # override
    def simulate_action(self):
        start_time = self.get_env().now

        with self.get_simulation().get_res_deposit().request() as req:
            yield req
            drawer_output = super().simulate_action()
            # check if there is a material to remove
            if len(drawer_output.get_items()) != 0:
                # choice random material
                mat_to_rmv = random.choice(drawer_output.get_items())
                # remove the material
                drawer_output.remove_material(mat_to_rmv)
                # estimate a time of the action
                yield self.env.timeout(self.get_duration())
            else:
                print(f"\nTime {self.env.now:5.2f} - No materials to remove\n")

        end_time = self.get_env().now

        yield self.simulation.get_store_history().put(dict(Action="InsertRandomMaterial",
                                                           Start=str(start_time),
                                                           Finish=str(end_time)))
