import copy
import unittest

from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.drawer import Drawer
from src.sim.status_warehouse.container.column import Column
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.warehouse import Warehouse


class TestColumn(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.column_config = {
            "height": 325,
            "x_offset": 125,
            "width": 250,
            "height_last_position": 75
        }
        self.column = Column(self.column_config, self.warehouse)

    def test_last_position_is_occupied(self):
        # arrange
        column_1 = self.column
        column_1.reset_container()
        column_2: Column = copy.deepcopy(column_1)
        for i in range(column_2.get_height_last_position()):
            column_2.get_container()[i] = DrawerEntry(column_2.get_offset_x(), i)

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
            container[i] = DrawerEntry(container[i].get_offset_x(), i)

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

    def test_add_drawer(self):
        # arrange
        drawer = Drawer()
        column = self.column
        index = column.get_height_container()-1

        # act
        column.add_drawer(drawer, index)

        # assert
        self.assertTrue(isinstance(column.get_container()[index], DrawerEntry))

    def test_remove_drawer(self):
        # arrange
        drawer = Drawer()
        column = self.column
        index = column.get_height_container() - 1

        # act
        column.add_drawer(drawer, index)

        # assert
        self.assertTrue(isinstance(column.get_container()[index], DrawerEntry))
        self.assertTrue(column.remove_drawer(drawer))

    def test_gen_materials_and_drawers(self):
        # arrange
        column = self.column
        materials_to_add = 3
        drawers_to_add = 3

        # act
        res = column.gen_materials_and_drawers(num_drawers=drawers_to_add, num_materials=materials_to_add)

        # assert
        self.assertEqual(res.drawers_inserted, drawers_to_add)
        self.assertEqual(res.materials_inserted, materials_to_add)

    def test_gen_materials_and_drawers_limit(self):
        # arrange
        column = self.column
        container_col = self.column.get_container()
        for i in range(len(container_col)):
            container_col[i] = DrawerEntry(container_col[i].get_offset_x(), i)
        container_col[-1] = EmptyEntry(container_col[-1].get_offset_x(), container_col[-1].get_pos_y())
        materials_to_add = 100
        drawers_to_add = 1

        # act
        res = column.gen_materials_and_drawers(num_drawers=drawers_to_add, num_materials=materials_to_add)

        # assert
        self.assertLessEqual(res.drawers_inserted, drawers_to_add)
        self.assertLessEqual(res.materials_inserted, materials_to_add)
