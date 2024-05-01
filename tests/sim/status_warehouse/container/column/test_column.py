import copy
import unittest

from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.warehouse import Warehouse
from src.sim.status_warehouse.container.column import Column


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