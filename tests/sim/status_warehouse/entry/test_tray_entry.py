import copy
from unittest import TestCase

from src.tray import Tray
from src.status_warehouse.entry.tray_entry import TrayEntry


class TestTrayEntry(TestCase):
    def setUp(self):
        self.offset_x = 200
        self.pos_y = 100
        self.tray = Tray()
        self.tray_entry = TrayEntry(self.offset_x, self.pos_y)
        self.tray_entry.add_tray(self.tray)

    def test_deepcopy(self):
        # arrange
        tray_entry = self.tray_entry

        # act
        deepcopy_tray_entry = copy.deepcopy(tray_entry)

        # assert
        self.assertIsInstance(deepcopy_tray_entry, TrayEntry)
        self.assertEqual(tray_entry, deepcopy_tray_entry)
        self.assertNotEqual(id(tray_entry), id(deepcopy_tray_entry))

    def test_eq(self):
        # arrange
        tray_entry = self.tray_entry

        # act

        # assert
        self.assertTrue(tray_entry.__eq__(tray_entry))

    def test_hash(self):
        # arrange
        tray_entry_1 = self.tray_entry
        tray_entry_2 = TrayEntry(self.offset_x+1, self.pos_y+1)

        # act

        # assert
        self.assertEqual(hash(tray_entry_1), hash(tray_entry_1))
        self.assertNotEqual(hash(tray_entry_1), hash(tray_entry_2))

    def test_get_tray(self):
        # arrange
        tray_entry = self.tray_entry

        # act
        tray_entry_get = tray_entry.get_tray()
        tray_entry_expected = tray_entry.tray

        # assert
        self.assertEqual(tray_entry_get, tray_entry_expected)

    def test_add_tray(self):
        # arrange
        tray_entry = self.tray_entry
        tray_entry.tray = None
        self.assertIsNone(tray_entry.get_tray())

        # act
        tray_entry.add_tray(self.tray)

        self.assertEqual(tray_entry.get_tray(), self.tray)