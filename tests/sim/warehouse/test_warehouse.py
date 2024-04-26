import copy
import unittest

from src.sim.status_warehouse.container.column import Column
from src.sim.warehouse import Warehouse, MinimumOffsetReturns


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

    def test_set_pos_y_floor(self):
        # arrange
        ex_pos_y_floor = self.warehouse.get_pos_y_floor()

        # act
        self.warehouse.set_pos_y_floor(15)

        # assert
        self.assertEqual(self.warehouse.get_pos_y_floor(), 15)
        self.assertRaises(Exception, self.warehouse.set_pos_y_floor, -15)
        # restore
        self.warehouse.set_pos_y_floor(ex_pos_y_floor)

    def test_add_column(self):
        # arrange
        col = self.warehouse.get_column(0)

        # act
        self.warehouse.add_column(col)

        # assert
        self.assertEqual(self.warehouse.get_column(-1), col)
        self.assertRaises(Exception, self.warehouse.add_column, None)
        # restore
        self.warehouse.pop_column()

    def test_get_minimum_offset(self):
        # arrange
        col = Column({
            'width': 200,
            'height': 1000,
            'x_offset': 1,
            'height_last_position': 75
        }, self.warehouse)
        self.warehouse.add_column(col)

        # act
        minimum_offset: MinimumOffsetReturns = self.warehouse.get_minimum_offset()

        # assert
        self.assertIn(col, self.warehouse.get_cols_container())
        self.assertEqual(minimum_offset.index, len(self.warehouse.get_cols_container())-1)
        self.assertEqual(minimum_offset.offset, 1)
