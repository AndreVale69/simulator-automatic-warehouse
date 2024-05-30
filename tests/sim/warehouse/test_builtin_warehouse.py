import copy
from unittest import TestCase

from src.warehouse import Warehouse


class TestBuiltinWarehouse(TestCase):
    def test_deepcopy(self):
        # arrange
        warehouse = Warehouse()

        # act
        deepcopy_warehouse = copy.deepcopy(warehouse)

        # assert
        self.assertIsInstance(deepcopy_warehouse, Warehouse)
        self.assertEqual(warehouse, deepcopy_warehouse)
        self.assertNotEqual(id(warehouse), id(deepcopy_warehouse))

    def test_eq(self):
        # arrange
        warehouse = Warehouse()

        # act

        # assert
        self.assertTrue(warehouse.__eq__(warehouse))

    def test_hash(self):
        # arrange
        warehouse_1 = Warehouse()
        warehouse_2 = Warehouse()

        # act

        # assert
        self.assertEqual(hash(warehouse_1), hash(warehouse_1))
        self.assertNotEqual(hash(warehouse_1), hash(warehouse_2))

