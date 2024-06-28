from unittest import TestCase
from unittest.mock import patch

from simpy import Environment

from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.simulation.actions.material.remove_material.remove_material import RemoveMaterial
from automatic_warehouse.warehouse import Warehouse


class TestRemoveMaterial(TestCase):
    def setUp(self):
        self.env = Environment()
        self.warehouse = Warehouse()
        self.duration = 10
        # use mock.patch to test abstract classes
        self.patch_remove_material = patch.multiple(RemoveMaterial, __abstractmethods__=set())
        self.patch_simulation = patch.multiple(Simulation, __abstractmethods__=set())
        self.patch_remove_material.start()
        self.patch_simulation.start()
        self.remove_material = RemoveMaterial(self.env, self.warehouse, Simulation(), self.duration)

    def tearDown(self):
        self.patch_remove_material.stop()
        self.patch_simulation.stop()

    def test_simulate_action_abstractmethod(self):
        # arrange
        remove_material = self.remove_material

        # act

        # assert
        self.assertRaises(NotImplementedError, remove_material.simulate_action)

    def test_get_duration(self):
        # arrange
        remove_material = self.remove_material
        duration_expected = self.duration

        # act
        duration = remove_material.get_duration()

        # assert
        self.assertEqual(duration, duration_expected)