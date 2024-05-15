from unittest import TestCase

from simpy import Environment

from src.sim.material import gen_rand_materials
from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.material.remove_material.remove_manual_material import RemoveManualMaterial
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse


class TestRemoveManualMaterial(TestCase):
    def setUp(self):
        warehouse = Warehouse()
        env = Environment()
        simulation = Simulation()
        duration = 2
        materials = gen_rand_materials(3)
        for material in materials:
            warehouse.get_carousel().get_deposit_drawer().add_material(material)
        self.remove_manual_material = RemoveManualMaterial(env, warehouse, simulation, duration, materials)

    def test_simulate_action(self):
        remove_manual_material = self.remove_manual_material
        simulation = remove_manual_material.get_simulation()
        env: Environment = simulation.get_environment()

        yield env.process(remove_manual_material.simulate_action())
        yield env.run()

        self.assertIn(ActionEnum.REMOVE_MANUAL_MATERIAL.value, simulation.get_store_history_dataframe()['Type of Action'])