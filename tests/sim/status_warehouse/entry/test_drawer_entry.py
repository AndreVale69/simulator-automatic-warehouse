import copy
import unittest

from src.sim.drawer import Drawer
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry


class TestDrawerEntry(unittest.TestCase):
    def setUp(self):
        self.offset_x = 200
        self.pos_y = 100
        self.drawer = Drawer()
        self.drawer_entry = DrawerEntry(self.offset_x, self.pos_y)
        self.drawer_entry.add_drawer(self.drawer)

    def test_deepcopy(self):
        # arrange
        drawer_entry = self.drawer_entry

        # act
        deepcopy_drawer_entry = copy.deepcopy(drawer_entry)

        # assert
        self.assertIsInstance(deepcopy_drawer_entry, DrawerEntry)
        self.assertEqual(drawer_entry, deepcopy_drawer_entry)
        self.assertNotEqual(id(drawer_entry), id(deepcopy_drawer_entry))

    def test_eq(self):
        # arrange
        drawer_entry = self.drawer_entry

        # act

        # assert
        self.assertTrue(drawer_entry.__eq__(drawer_entry))

    def test_hash(self):
        # arrange
        drawer_entry_1 = self.drawer_entry
        drawer_entry_2 = DrawerEntry(self.offset_x+1, self.pos_y+1)

        # act

        # assert
        self.assertEqual(hash(drawer_entry_1), hash(drawer_entry_1))
        self.assertNotEqual(hash(drawer_entry_1), hash(drawer_entry_2))

    def test_get_drawer(self):
        # arrange
        drawer_entry = self.drawer_entry

        # act
        drawer_entry_get = drawer_entry.get_drawer()
        drawer_entry_expected = drawer_entry.drawer

        # assert
        self.assertEqual(drawer_entry_get, drawer_entry_expected)

    def test_add_drawer(self):
        # arrange
        drawer_entry = self.drawer_entry
        drawer_entry.drawer = None
        self.assertIsNone(drawer_entry.get_drawer())

        # act
        drawer_entry.add_drawer(self.drawer)

        self.assertEqual(drawer_entry.get_drawer(), self.drawer)