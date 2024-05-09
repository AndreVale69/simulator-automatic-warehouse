from unittest import TestCase

from simpy import Environment

from src.sim.simulation.actions.material.remove_material.remove_material import RemoveMaterial
from src.sim.warehouse import Warehouse


class TestRemoveMaterial(TestCase):
    def setUp(self):
        self.env = Environment()
        self.warehouse = Warehouse()
        self.duration = 10
        self.remove_material = RemoveMaterial(self.env, self.warehouse, None, self.duration)

    def test_get_duration(self):
        # arrange
        remove_material = self.remove_material
        duration_expected = self.duration

        # act
        duration = remove_material.get_duration()

        # assert
        self.assertEqual(duration, duration_expected)