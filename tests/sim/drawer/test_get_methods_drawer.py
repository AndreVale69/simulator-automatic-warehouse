from unittest import TestCase

from src.sim.drawer import Drawer
from src.sim.material import gen_rand_materials


class TestGetMethodsDrawer(TestCase):
    def setUp(self):
        self.drawer = Drawer(gen_rand_materials(2))

    def test_get_items(self):
        # arrange
        drawer = self.drawer

        # act
        items_get = drawer.get_items()
        items_expected = drawer.items

        # assert
        self.assertEqual(items_get, items_expected)

    def test_get_max_height(self):
        # arrange
        drawer = self.drawer

        # act
        max_height_get = drawer.get_max_height()
        max_height_expected = drawer.max_height

        # assert
        self.assertEqual(max_height_get, max_height_expected)

    def test_get_num_space_occupied(self):
        # arrange
        drawer = self.drawer

        # act
        num_space_occupied_get = drawer.get_num_space_occupied()
        num_space_occupied_expected = drawer.num_space

        # assert
        self.assertEqual(num_space_occupied_get, num_space_occupied_expected)

    def test_get_first_drawerEntry(self):
        # arrange
        drawer = self.drawer

        # act
        first_drawerEntry_get = drawer.get_first_drawerEntry()
        first_drawerEntry_expected = drawer.first_drawerEntry

        # assert
        self.assertEqual(first_drawerEntry_get, first_drawerEntry_expected)

    def test_get_best_offset_x(self):
        # arrange
        drawer = self.drawer

        # act
        best_offset_x_get = drawer.get_best_offset_x()
        best_offset_x_expected = drawer.best_offset_x

        # assert
        self.assertEqual(best_offset_x_get, best_offset_x_expected)

    def test_get_best_y(self):
        # arrange
        drawer = self.drawer

        # act
        best_y_get = drawer.get_best_y()
        best_y_expected = drawer.best_y

        # assert
        self.assertEqual(best_y_get, best_y_expected)

    def test_get_num_materials(self):
        # arrange
        drawer = self.drawer

        # act
        num_materials_get = drawer.get_num_materials()
        num_materials_expected = len(drawer.items)

        # assert
        self.assertEqual(num_materials_get, num_materials_expected)
