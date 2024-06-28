import copy
from unittest import TestCase

from automatic_warehouse.status_warehouse.container.column import Column
from automatic_warehouse.status_warehouse.entry.empty_entry import EmptyEntry
from automatic_warehouse.status_warehouse.entry.tray_entry import TrayEntry
from status_warehouse.tray import Tray
from automatic_warehouse.warehouse import Warehouse
from automatic_warehouse.warehouse_configuration_singleton import (
    ColumnConfiguration,
    TrayConfiguration,
    WarehouseConfigurationSingleton
)


class TestColumn(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.column_config = ColumnConfiguration(
            length=450,
            height = 325,
            x_offset = 125,
            width = 250,
            height_last_position = 75
        )
        self.column = Column(self.column_config, self.warehouse)

    def test_column_info_parameter(self):
        # arrange
        param_1: int = 1
        param_2: str = 'str'
        param_3: float = 3.6
        param_4: int = 4
        param_5: float = 455.1

        # act

        # assert
        self.assertRaises(TypeError, ColumnConfiguration, param_1, param_2, param_3, param_4, param_5)

    def test_last_position_is_occupied(self):
        # arrange
        column_1 = self.column
        column_1.reset_container()
        column_2: Column = copy.deepcopy(column_1)
        for i in range(column_2.get_height_last_position()):
            column_2.get_container()[i] = TrayEntry(column_2.get_offset_x(), i)

        # act
        last_position_is_occupied_col1 = column_1.last_position_is_occupied()
        last_position_is_occupied_col2 = column_2.last_position_is_occupied()

        # assert
        self.assertFalse(last_position_is_occupied_col1)
        self.assertTrue(last_position_is_occupied_col2)

    def test_is_full(self):
        # arrange
        column = self.column
        container = column.get_container()
        for i in range(len(container)):
            container[i] = TrayEntry(container[i].get_offset_x(), i)

        # act
        is_full = column.is_full()

        # assert
        self.assertTrue(is_full)

    def test_is_empty(self):
        # arrange
        column = self.column
        column.reset_container()

        # act
        is_empty = column.is_empty()

        # assert
        self.assertTrue(is_empty)

    def test_add_tray(self):
        # arrange
        config = WarehouseConfigurationSingleton.get_instance().get_configuration()
        tray = Tray()
        column = self.column
        index = column.get_num_entries() - 1

        # act
        column.add_tray(tray, index)

        # assert
        self.assertTrue(isinstance(column.get_container()[index], TrayEntry))
        self.assertRaises(ValueError, column.add_tray, Tray(TrayConfiguration(
            length=column.length,
            width=column.width,
            maximum_height=column.height_container
        )))

    def test_remove_tray(self):
        # arrange
        tray = Tray()
        column = self.column
        index = column.get_num_entries() - 1

        # act
        column.add_tray(tray, index)

        # assert
        self.assertTrue(isinstance(column.get_container()[index], TrayEntry))
        self.assertTrue(column.remove_tray(tray))

    def test_gen_materials_and_trays(self):
        # arrange
        column = self.column
        materials_to_add = 3
        trays_to_add = 3

        # act
        res = column.gen_materials_and_trays(num_trays=trays_to_add, num_materials=materials_to_add)

        # assert
        self.assertEqual(res.trays_inserted, trays_to_add)
        self.assertEqual(res.materials_inserted, materials_to_add)

    def test_gen_materials_and_trays_limit(self):
        # arrange
        column = self.column
        container_col = self.column.get_container()
        for i in range(len(container_col)):
            container_col[i] = TrayEntry(container_col[i].get_offset_x(), i)
        container_col[-1] = EmptyEntry(container_col[-1].get_offset_x(), container_col[-1].get_pos_y())
        materials_to_add = 100
        trays_to_add = 1

        # act
        res = column.gen_materials_and_trays(num_trays=trays_to_add, num_materials=materials_to_add)

        # assert
        self.assertLessEqual(res.trays_inserted, trays_to_add)
        self.assertLessEqual(res.materials_inserted, materials_to_add)
