from simpy import Environment

from src.drawer import Drawer
from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse


class InsertMaterial(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        super().__init__(env, warehouse, simulation)

    # override
    def simulate_action(self):
        from src.material import gen_rand_material

        print(f"Time {self.env.now:5.2f} - Start putting materials inside a drawer")
        # generate random material
        mat_to_put = gen_rand_material()
        # take the drawer that is outside
        drawer_output: Drawer = self.get_warehouse().get_carousel().get_deposit_entry().get_drawer()
        # add the material
        drawer_output.add_material(mat_to_put)
        # TODO: "crea" evento estrai cassetto
        # add a reference to the drawer
        self.get_warehouse().set_drawer_of_support(drawer_output)
        # TODO: timeout nel costrutto con param
        # estimate a time of the action
        yield self.env.timeout(2)
