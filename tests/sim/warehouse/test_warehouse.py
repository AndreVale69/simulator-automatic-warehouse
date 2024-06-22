from unittest import TestCase

from automatic_warehouse.status_warehouse.container.column import Column
from automatic_warehouse.status_warehouse.entry.empty_entry import EmptyEntry
from automatic_warehouse.status_warehouse.entry.tray_entry import TrayEntry
from automatic_warehouse.warehouse import Warehouse
from automatic_warehouse.warehouse_configuration_singleton import WarehouseConfigurationSingleton, ColumnConfiguration


class TestWarehouse(TestCase):
    def test_set_pos_y_floor(self):
        # arrange
        warehouse = Warehouse()

        # act
        warehouse.set_pos_y_floor(15)

        # assert
        self.assertEqual(warehouse.get_pos_y_floor(), 15)
        self.assertRaises(Exception, warehouse.set_pos_y_floor, -15)

    def test_add_column(self):
        # arrange
        warehouse = Warehouse()
        col_0 = warehouse.get_column(0)
        col = Column(
            ColumnConfiguration(
                length=col_0.get_length(),
                height=col_0.get_height_container(),
                x_offset=col_0.get_offset_x() + 500,
                width=col_0.get_width(),
                height_last_position=col_0.get_height_last_position()
            ),
            warehouse
        )

        # act
        warehouse.add_column(col)

        # assert
        self.assertEqual(warehouse.get_column(-1), col)
        self.assertRaises(Exception, warehouse.add_column, None)
        self.assertRaises(ValueError, warehouse.add_column, col)
        self.assertRaises(ValueError, warehouse.add_column, col_0)

    def test_pop_column(self):
        # arrange
        warehouse = Warehouse()
        num_cols_pre = warehouse.get_num_columns()
        num_cols_expected = num_cols_pre - 1

        # act
        column_pop = warehouse.pop_column(0)
        num_cols_actual = warehouse.get_num_columns()

        # assert
        self.assertNotIn(column_pop, warehouse.get_cols_container())
        self.assertEqual(num_cols_actual, num_cols_expected)
        self.assertNotEqual(num_cols_actual, num_cols_pre)
        self.assertRaises(IndexError, warehouse.pop_column, num_cols_pre)

    def test_remove_column(self):
        # arrange
        warehouse = Warehouse()
        num_cols_pre = warehouse.get_num_columns()
        num_cols_expected = num_cols_pre - 1
        col_to_remove = warehouse.get_column(0)

        # act
        warehouse.remove_column(col_to_remove)
        num_cols_actual = warehouse.get_num_columns()

        # assert
        self.assertNotIn(col_to_remove, warehouse.get_cols_container())
        self.assertEqual(num_cols_actual, num_cols_expected)
        self.assertNotEqual(num_cols_actual, num_cols_pre)
        self.assertRaises(IndexError, warehouse.pop_column, num_cols_pre)

    def test_is_full(self):
        # arrange
        warehouse = Warehouse()
        for col in warehouse.get_cols_container():
            for index, entry in enumerate(col.get_container()):
                if isinstance(entry, EmptyEntry):
                    col.get_container()[index] = TrayEntry(entry.get_offset_x(), entry.get_pos_y())

        # act

        # assert
        self.assertTrue(warehouse.is_full())

    def test_gen_rand(self):
        # arrange
        warehouse = Warehouse()
        config = WarehouseConfigurationSingleton.get_instance().get_configuration().simulation
        trays_to_gen = config.trays_to_gen + config.gen_bay + config.gen_buffer
        materials_to_gen = config.materials_to_gen
        trays_find = 0
        materials_find = 0

        # act
        for col in warehouse.get_cols_container():
            trays_find += col.get_num_trays()
            for tray in col.get_trays():
                materials_find += tray.get_num_materials()
        trays_find += warehouse.get_carousel().is_buffer_full()
        trays_find += warehouse.get_carousel().is_bay_full()

        # assert
        self.assertEqual(trays_to_gen, trays_find)
        self.assertEqual(materials_to_gen, materials_find)

    def test_gen_rand_full(self):
        # arrange
        warehouse = Warehouse()
        warehouse.gen_rand(True, True, 1000, 1000)

        # act
        res = warehouse.is_full()

        # assert
        self.assertTrue(res)

    def test_choice_random_tray(self):
        # arrange
        trays = []
        warehouse = Warehouse()

        # act
        for col in warehouse.get_cols_container():
            trays.extend(col.get_trays())

        # assert
        self.assertIn(warehouse.choice_random_tray(), trays)

    def test_choice_random_tray_with_empty_column(self):
        # arrange
        warehouse = Warehouse()
        warehouse.add_column(Column(ColumnConfiguration(
            length=200,
            height = 325,
            x_offset = warehouse.get_column(0).get_offset_x() + 200,
            width = 250,
            height_last_position = 75
        ), warehouse))
        trays = []

        # act
        for col in warehouse.get_cols_container():
            trays.extend(col.get_trays())

        # assert
        self.assertIn(warehouse.choice_random_tray(), trays)

    def test_cleanup(self):
        # arrange
        warehouse = Warehouse()

        # act
        warehouse.cleanup()

        # assert
        self.assertEqual(warehouse.get_num_trays(), 0)
