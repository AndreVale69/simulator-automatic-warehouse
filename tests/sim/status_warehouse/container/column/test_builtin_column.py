import copy
from unittest import TestCase

from automatic_warehouse.status_warehouse.container.column import Column
from automatic_warehouse.warehouse import Warehouse
from automatic_warehouse.warehouse_configuration_singleton import ColumnConfiguration


class TestBuiltinColumn(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.column_config = ColumnConfiguration(
            length=200,
            height = 325,
            x_offset = 125,
            width = 250,
            height_last_position = 75
        )
        self.column = Column(self.column_config, self.warehouse)

    def test_deepcopy(self):
        # arrange
        column = self.column

        # act
        deepcopy_column = copy.deepcopy(column)

        # assert
        self.assertIsInstance(deepcopy_column, Column)
        self.assertEqual(column, deepcopy_column)
        self.assertNotEqual(id(column), id(deepcopy_column))

    def test_eq(self):
        # arrange
        column = self.column

        # act

        # assert
        self.assertTrue(column.__eq__(column))

    def test_hash(self):
        # arrange
        column_1 = self.column
        column_2 = Column(ColumnConfiguration(
            length=300,
            height = 350,
            x_offset = 150,
            width = 275,
            height_last_position = 100
        ), Warehouse())

        # act

        # assert
        self.assertEqual(hash(column_1), hash(column_1))
        self.assertNotEqual(hash(column_1), hash(column_2))
