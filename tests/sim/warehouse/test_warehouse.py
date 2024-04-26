import copy
import unittest

from src.sim.warehouse import Warehouse


class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()

    def test_deepcopy(self):
        # arrange

        # act
        deepcopy_warehouse = copy.deepcopy(self.warehouse)

        # assert
        self.assertIsInstance(deepcopy_warehouse, Warehouse)
        self.assertEqual(self.warehouse, deepcopy_warehouse)
        self.assertNotEqual(id(self.warehouse), id(deepcopy_warehouse))
