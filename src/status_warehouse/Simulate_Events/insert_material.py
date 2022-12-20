from simpy import Environment

from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.simulation import Simulation


class InsertMaterial(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor: Simulation):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self):
        from src.status_warehouse.Entry.drawerEntry import DrawerEntry

        print(f"Time {self.env.now:5.2f} - Start putting materials inside a drawer")
        # generate random material
        mat_to_put = self.get_warehouse().gen_rand_material()
        # take the drawer that is outside
        drawer_output: Drawer = DrawerEntry.get_drawer(self.get_warehouse().get_carousel().get_container()[0])
        # add the material
        drawer_output.add_material(mat_to_put)
        # add a reference to the drawer
        self.get_warehouse().set_drawer_of_support(drawer_output)
        # estimate a time of the action
        yield self.env.timeout(2)
