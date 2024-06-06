from unittest import TestCase

from simpy import Environment

from src.simulation.simulation import Simulation
from src.simulation.actions.material.insert_material.insert_material import InsertMaterial
from src.warehouse import Warehouse


class TestInsertMaterial(TestCase):
    def setUp(self):
        self.env = Environment()
        self.warehouse = Warehouse()
        self.duration = 10
        self.insert_material = InsertMaterial(self.env, self.warehouse, Simulation(), self.duration)

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