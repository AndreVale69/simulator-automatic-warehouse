import copy
from unittest import TestCase

from automatic_warehouse.status_warehouse.entry.empty_entry import EmptyEntry


class TestEmptyEntry(TestCase):
    def setUp(self):
        self.offset_x = 200
        self.pos_y = 100
        self.empty_entry = EmptyEntry(self.offset_x, self.pos_y)

    def test_deepcopy(self):
        # arrange
        empty_entry = self.empty_entry

        # act
        deepcopy_empty_entry = copy.deepcopy(empty_entry)

        # assert
        self.assertIsInstance(deepcopy_empty_entry, EmptyEntry)
        self.assertEqual(empty_entry, deepcopy_empty_entry)
        self.assertNotEqual(id(empty_entry), id(deepcopy_empty_entry))

    def test_eq(self):
        # arrange
        empty_entry = self.empty_entry

        # act

        # assert
        self.assertTrue(empty_entry.__eq__(empty_entry))

    def test_hash(self):
        # arrange
        empty_entry_1 = self.empty_entry
        empty_entry_2 = EmptyEntry(self.offset_x+1, self.pos_y+1)

        # act

        # assert
        self.assertEqual(hash(empty_entry_1), hash(empty_entry_1))
        self.assertNotEqual(hash(empty_entry_1), hash(empty_entry_2))
