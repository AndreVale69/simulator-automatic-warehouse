from simpy import Environment

# from src.drawer import Drawer
from src.sim.material import Material
from src.sim.simulation import Simulation
from src.sim.status_warehouse.simulate_events.material.insert_material.insert_material import InsertMaterial
from src.sim.warehouse import Warehouse


class InsertManualMaterial(InsertMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation,
                 duration: int, materials: list[Material]):
        """
        The insert manual material action is the movement
        performed by the person who has put a material from his hand to the deposit (bay).

        :type env: Environment
        :type warehouse: Warehouse
        :type simulation: Simulation
        :type duration: int
        :type materials: list[Material]
        :param env: the simulation environment (SimPy Environment).
        :param warehouse: the warehouse where the action is performed.
        :param simulation: the simulation where the action is performed.
        :param duration: the duration of the action in seconds.
        :param materials: the materials to be inserted.
        """
        super().__init__(env, warehouse, simulation, duration)
        self.materials = materials.copy()

    def get_materials(self) -> list[Material]:
        """
        Get the list of materials to be inserted.

        :rtype: list[Material]
        :return: the materials to be inserted.
        """
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
