from unittest import TestCase

from src.status_warehouse.entry.entry import Entry


class TestTrayEntry(TestCase):
    def setUp(self):
        self.offset_x = 200
        self.pos_y = 100
        self.entry = Entry(self.offset_x, self.pos_y)

    def test_eq(self):
        # arrange
        entry = self.entry

        # act

        # assert
        self.assertTrue(entry.__eq__(entry))

    def test_hash(self):
        # arrange
        entry_1 = self.entry
        entry_2 = Entry(self.offset_x+1, self.pos_y+1)

        # act

        # assert
        self.assertEqual(hash(entry_1), hash(entry_1))
        self.assertNotEqual(hash(entry_1), hash(entry_2))

    def test_get_offset_x(self):
        # arrange
        entry = self.entry

        # act
        offset_x_get = entry.get_offset_x()
        offset_x_expected = entry.offset_x

        # assert
        self.assertEqual(offset_x_get, offset_x_expected)

    def test_get_pos_y(self):
        # arrange
        entry = self.entry

        # act
        pos_y_get = entry.get_offset_x()
        pos_y_expected = entry.offset_x

        # assert
        self.assertEqual(pos_y_get, pos_y_expected)