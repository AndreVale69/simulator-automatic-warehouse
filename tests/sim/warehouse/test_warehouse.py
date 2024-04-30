import unittest

from src.sim.status_warehouse.container.column import Column
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.warehouse import Warehouse
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class TestWarehouse(unittest.TestCase):
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

    def test_gen_rand(self):
        # arrange
        warehouse = Warehouse()
        config = WarehouseConfigurationSingleton.get_instance().get_configuration()
        drawers_to_gen = config["simulation"]["drawers_to_gen"]
        materials_to_gen = config["simulation"]["materials_to_gen"]
        drawers_find = 0
        materials_find = 0

        # act
        for col in warehouse.get_cols_container():
            drawers_find += col.get_num_drawers()
            for drawer in col.get_drawers():
                materials_find += drawer.get_num_materials()

        # assert
        self.assertEqual(drawers_to_gen, drawers_find)
        self.assertEqual(materials_to_gen, materials_find)
