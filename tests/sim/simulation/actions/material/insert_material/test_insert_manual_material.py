from unittest import TestCase

from simpy import Environment

from src.sim.simulation.actions.action_enum import ActionEnum
from src.sim.simulation.actions.material.insert_material.insert_manual_material import InsertManualMaterial
from src.sim.material import gen_rand_materials
from src.sim.simulation.simulation import Simulation
from src.sim.warehouse import Warehouse


class TestInsertManualMaterial(TestCase):
    def setUp(self):
        warehouse = Warehouse()
        env = Environment()
        simulation = Simulation()
        duration = 2
        materials = gen_rand_materials(3)
        self.insert_manual_material = InsertManualMaterial(env, warehouse, simulation, duration, materials)

    def test_simulate_action(self):
        insert_manual_material = self.insert_manual_material
        simulation = insert_manual_material.get_simulation()
        env: Environment = simulation.get_environment()

        yield env.process(insert_manual_material.simulate_action())
        yield env.run()

        self.assertIn(ActionEnum.INSERT_MANUAL_MATERIAL.value, simulation.get_store_history_dataframe()['Type of Action'])