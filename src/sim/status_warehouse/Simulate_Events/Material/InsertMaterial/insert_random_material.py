from simpy import Environment
import datetime

# from src.drawer import Drawer
from sim.simulation import Simulation
from sim.status_warehouse.Simulate_Events.Material.InsertMaterial.insert_material import InsertMaterial
from sim.warehouse import Warehouse


class InsertRandomMaterial(InsertMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        super().__init__(env, warehouse, simulation, duration)

    # override
    def simulate_action(self):
        from sim.material import gen_rand_material

        start_time = datetime.datetime.now() + datetime.timedelta(seconds=self.get_env().now)

        with self.get_simulation().get_res_deposit().request() as req:
            yield req
            drawer_output = super().simulate_action()
            # generate random material
            mat_to_put = gen_rand_material()
            # add the material
            drawer_output.add_material(mat_to_put)
            # estimate a time of the action
            yield self.env.timeout(self.get_duration())

        end_time = datetime.datetime.now() + datetime.timedelta(seconds=self.get_env().now)

        yield self.simulation.get_store_history().put({
            'Type of Action': "InsertRandomMaterial",
            'Start'         : start_time,
            'Finish'        : end_time
        })
