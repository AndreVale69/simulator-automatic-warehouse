from unittest import TestCase

from automatic_warehouse.status_warehouse.container.column import Column
from automatic_warehouse.warehouse import Warehouse
from automatic_warehouse.warehouse_configuration_singleton import ColumnConfiguration


class TestGetMethodsColumn(TestCase):
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

    def test_get_height_last_position(self):
        # arrange
        column = self.column

        # act
        height_last_position_get = column.get_height_last_position()
        height_last_position_expected = column.height_last_position

        # assert
        self.assertEqual(height_last_position_get, height_last_position_expected)

    def test_get_num_entries_free(self):
        # arrange
        column = self.column
        column.reset_container()

        # act
        num_entries_free_get = column.get_num_entries_free()
        num_entries_free_expected = column.get_num_entries() - column.get_height_last_position() + 1

        # assert
        self.assertEqual(num_entries_free_get, num_entries_free_expected)
