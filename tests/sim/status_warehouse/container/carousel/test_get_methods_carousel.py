import unittest

from src.sim.drawer import Drawer
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.status_warehouse.container.carousel import Carousel
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.warehouse import Warehouse


class TestGetMethodsCarousel(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.carousel_config = {
            "deposit_height": 150,
            "buffer_height": 150,
            "x_offset": 125,
            "width": 250
        }
        self.carousel = Carousel(self.carousel_config, self.warehouse)

    def test_get_buffer(self):
        # arrange
        carousel = self.carousel

        # act
        buffer_get = carousel.get_buffer()
        buffer_expected = carousel.buffer

        # assert
        self.assertEqual(buffer_get, buffer_expected)

    def test_get_deposit(self):
        # arrange
        carousel = self.carousel

        # act
        deposit_get = carousel.get_deposit()
        deposit_expected = carousel.deposit

        # assert
        self.assertEqual(deposit_get, deposit_expected)

    def test_get_hole(self):
        # arrange
        carousel = self.carousel

        # act
        hole_get = carousel.get_hole()
        hole_expected = carousel.hole

        # assert
        self.assertEqual(hole_get, hole_expected)

    def test_get_deposit_entry(self):
        # arrange
        carousel = self.carousel

        # act
        deposit_entry_get = carousel.get_deposit_entry()
        deposit_entry_expected = carousel.container[0]

        # assert
        self.assertEqual(deposit_entry_get, deposit_entry_expected)

    def test_get_deposit_drawer(self):
        # arrange
        deposit_drawer = Drawer()
        carousel = self.carousel
        carousel.reset_container()
        carousel.add_drawer(deposit_drawer)

        # act
        deposit_drawer_get = carousel.get_deposit_drawer()
        deposit_drawer_expected = deposit_drawer

        # assert
        self.assertEqual(deposit_drawer_get, deposit_drawer_expected)

    def test_get_buffer_entry(self):
        # arrange
        carousel = self.carousel

        # act
        buffer_entry_get = carousel.get_buffer_entry()
        buffer_entry_expected = carousel.container[1]

        # assert
        self.assertEqual(buffer_entry_get, buffer_entry_expected)

    def test_get_buffer_drawer(self):
        # arrange
        deposit_drawer = Drawer()
        buffer_drawer = Drawer()
        carousel = self.carousel
        carousel.reset_container()
        carousel.add_drawer(deposit_drawer)
        carousel.add_drawer(buffer_drawer)

        # act
        buffer_drawer_get = carousel.get_buffer_drawer()
        buffer_drawer_expected = buffer_drawer

        # assert
        self.assertEqual(buffer_drawer_get, buffer_drawer_expected)

    def test_get_num_drawers(self):
        # arrange
        carousel = self.carousel

        # act
        num_drawers_get = carousel.get_num_drawers()
        num_drawers_expected = (isinstance(carousel.get_deposit_entry(), DrawerEntry) +
                                isinstance(carousel.get_buffer_entry(), DrawerEntry))

        # assert
        self.assertEqual(num_drawers_get, num_drawers_expected)

    def test_get_num_entries_free(self):
        # arrange
        carousel = self.carousel

        # act
        num_entries_free_get = carousel.get_num_entries_free()
        num_entries_free_expected = sum(isinstance(entry, EmptyEntry) for entry in carousel.get_container())

        # assert
        self.assertEqual(num_entries_free_get, num_entries_free_expected)
