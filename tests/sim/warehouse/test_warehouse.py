from unittest import TestCase

from src.sim.status_warehouse.container.column import Column
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.warehouse import Warehouse
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


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
        col = warehouse.get_column(0)

        # act
        warehouse.add_column(col)

        # assert
        self.assertEqual(warehouse.get_column(-1), col)
        self.assertRaises(Exception, warehouse.add_column, None)

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
                    col.get_container()[index] = DrawerEntry(entry.get_offset_x(), entry.get_pos_y())

        # act

        # assert
        self.assertTrue(warehouse.is_full())

    def test_gen_rand(self):
        # arrange
        warehouse = Warehouse()
        config = WarehouseConfigurationSingleton.get_instance().get_configuration()
        drawers_to_gen = config["simulation"]["drawers_to_gen"] + config["simulation"]["gen_deposit"] + config["simulation"]["gen_buffer"]
        materials_to_gen = config["simulation"]["materials_to_gen"]
        drawers_find = 0
        materials_find = 0

        # act
        for col in warehouse.get_cols_container():
            drawers_find += col.get_num_drawers()
            for drawer in col.get_drawers():
                materials_find += drawer.get_num_materials()
        drawers_find += warehouse.get_carousel().is_buffer_full()
        drawers_find += warehouse.get_carousel().is_deposit_full()

        # assert
        self.assertEqual(drawers_to_gen, drawers_find)
        self.assertEqual(materials_to_gen, materials_find)

    def test_gen_rand_full(self):
        # arrange
        warehouse = Warehouse()
        warehouse.gen_rand(True, True, 1000, 1000)

        # act
        res = warehouse.is_full()

        # assert
        self.assertTrue(res)

    def test_choice_random_drawer(self):
        # arrange
        drawers = []
        warehouse = Warehouse()

        # act
        for col in warehouse.get_cols_container():
            drawers.extend(col.get_drawers())

        # assert
        self.assertIn(warehouse.choice_random_drawer(), drawers)

    def test_choice_random_drawer_with_empty_column(self):
        # arrange
        warehouse = Warehouse()
        warehouse.add_column(Column({
            "height": 325,
            "x_offset": 125,
            "width": 250,
            "height_last_position": 75
        }, warehouse))
        drawers = []

        # act
        for col in warehouse.get_cols_container():
            drawers.extend(col.get_drawers())

        # assert
        self.assertIn(warehouse.choice_random_drawer(), drawers)

    def test_cleanup(self):
        # arrange
        warehouse = Warehouse()

        # act
        warehouse.cleanup()

        # assert
        self.assertEqual(warehouse.get_num_drawers(), 0)
