from unittest import TestCase

from src.material import gen_rand_materials
from src.tray import Tray


class TestGetMethodsTray(TestCase):
    def setUp(self):
        self.tray = Tray(items=gen_rand_materials(2))

    def test_get_items(self):
        # arrange
        tray = self.tray

        # act
        items_get = tray.get_items()
        items_expected = tray.items

        # assert
        self.assertEqual(items_get, items_expected)

    def test_get_max_height(self):
        # arrange
        tray = self.tray

        # act
        max_height_get = tray.get_max_height()
        max_height_expected = tray.height

        # assert
        self.assertEqual(max_height_get, max_height_expected)

    def test_get_num_space_occupied(self):
        # arrange
        tray = self.tray

        # act
        num_space_occupied_get = tray.get_num_space_occupied()
        num_space_occupied_expected = tray.num_space

        # assert
        self.assertEqual(num_space_occupied_get, num_space_occupied_expected)

    def test_get_first_trayEntry(self):
        # arrange
        tray = self.tray

        # act
        first_tray_entry_get = tray.get_first_tray_entry()
        first_tray_entry_expected = tray.first_trayEntry

        # assert
        self.assertEqual(first_tray_entry_get, first_tray_entry_expected)

    def test_get_best_offset_x(self):
        # arrange
        tray = self.tray

        # act
        best_offset_x_get = tray.get_best_offset_x()
        best_offset_x_expected = tray.best_offset_x

        # assert
        self.assertEqual(best_offset_x_get, best_offset_x_expected)

    def test_get_best_y(self):
        # arrange
        tray = self.tray

        # act
        best_y_get = tray.get_best_y()
        best_y_expected = tray.best_y

        # assert
        self.assertEqual(best_y_get, best_y_expected)

    def test_get_num_materials(self):
        # arrange
        tray = self.tray

        # act
        num_materials_get = tray.get_num_materials()
        num_materials_expected = len(tray.items)

        # assert
        self.assertEqual(num_materials_get, num_materials_expected)
