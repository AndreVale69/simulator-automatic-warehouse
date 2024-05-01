import unittest

from src.sim.drawer import Drawer
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.container.carousel import Carousel
from src.sim.warehouse import Warehouse


class TestCarousel(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.carousel_config = {
            "deposit_height": 150,
            "buffer_height": 150,
            "x_offset": 125,
            "width": 250
        }
        self.carousel = Carousel(self.carousel_config, self.warehouse)

    def test_is_full(self):
        # arrange
        carousel = self.carousel

        # act
        is_full = carousel.is_full()
        expected_is_full = carousel.is_buffer_full() and carousel.is_deposit_full()

        # assert
        self.assertEqual(is_full, expected_is_full)

    def test_is_empty(self):
        # arrange
        carousel = self.carousel

        # act
        is_empty = carousel.is_empty()
        expected_is_empty = not carousel.is_buffer_full() and not carousel.is_deposit_full()

        # assert
        self.assertEqual(is_empty, expected_is_empty)

    def test_is_buffer_full(self):
        # arrange
        carousel = self.carousel

        # act
        is_buffer_full = carousel.is_buffer_full()
        expected_is_buffer_full = isinstance(carousel.get_buffer_entry(), DrawerEntry)

        # assert
        self.assertEqual(is_buffer_full, expected_is_buffer_full)

    def test_is_deposit_full(self):
        # arrange
        carousel = self.carousel

        # act
        is_deposit_full = carousel.is_deposit_full()
        expected_is_deposit_full = isinstance(carousel.get_deposit_entry(), DrawerEntry)

        # assert
        self.assertEqual(is_deposit_full, expected_is_deposit_full)

    def test_add_drawer(self):
        # arrange
        drawer = Drawer()
        warehouse = self.warehouse
        carousel = warehouse.get_carousel()

        # act
        carousel.reset_container()
        self.assertTrue(carousel.is_empty())
        carousel.add_drawer(drawer)

        # assert
        self.assertTrue(carousel.is_deposit_full())
        self.assertFalse(carousel.is_buffer_full())

    def test_add_drawer_full(self):
        # arrange
        drawer_1 = Drawer()
        drawer_2 = Drawer()
        warehouse = self.warehouse
        carousel = warehouse.get_carousel()

        # act
        carousel.reset_container()
        self.assertTrue(carousel.is_empty())
        carousel.add_drawer(drawer_1)
        carousel.add_drawer(drawer_2)

        # assert
        self.assertTrue(carousel.is_full())

    def test_remove_drawer(self):
        # arrange
        drawer_1 = Drawer()
        drawer_2 = Drawer()
        carousel = self.carousel
        carousel.reset_container()
        self.assertTrue(carousel.is_empty())
        carousel.add_drawer(drawer_1)
        carousel.add_drawer(drawer_2)
        self.assertTrue(carousel.is_deposit_full())
        self.assertTrue(carousel.is_buffer_full())

        # act
        successful_remove_1 = carousel.remove_drawer(drawer_1)
        successful_remove_2 = carousel.remove_drawer(drawer_2)
        failure_remove = carousel.remove_drawer(drawer_1)

        # assert
        self.assertTrue(successful_remove_1)
        self.assertTrue(successful_remove_2)
        self.assertFalse(failure_remove)
