from unittest import TestCase
from unittest.mock import patch

from simpy import Environment

from automatic_warehouse.simulation.actions.material.insert_material.insert_material import InsertMaterial
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse


class InsertMaterialWorkAround(InsertMaterial):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, duration: int):
        super().__init__(env, warehouse, simulation, duration)

    def simulate_action(self, tray=None, destination=None):
        super(tray, destination)


class TestInsertMaterial(TestCase):
    def setUp(self):
        self.env = Environment()
        self.warehouse = Warehouse()
        self.duration = 10
        # use mock.patch to test abstract classes
        self.patch_insert_material = patch.multiple(InsertMaterial, __abstractmethods__=set())
        self.patch_simulation = patch.multiple(Simulation, __abstractmethods__=set())
        self.patch_insert_material.start()
        self.patch_simulation.start()
        self.insert_material = InsertMaterial(self.env, self.warehouse, Simulation(), self.duration)

    def tearDown(self):
        self.patch_insert_material.stop()
        self.patch_simulation.stop()

    def test_simulate_action_abstractmethod(self):
        # arrange
        insert_material = self.insert_material

        # act

        # assert
        self.assertRaises(NotImplementedError, insert_material.simulate_action)

    def test_get_duration(self):
        # arrange
        insert_material = self.insert_material
        duration_expected = self.duration

        # act
        duration = insert_material.get_duration()

        # assert
        self.assertEqual(duration, duration_expected)