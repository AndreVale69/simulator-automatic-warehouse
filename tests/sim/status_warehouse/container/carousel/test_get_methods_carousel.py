from unittest import TestCase

from automatic_warehouse.status_warehouse.container.carousel import Carousel, CarouselConfiguration
from automatic_warehouse.status_warehouse.entry.empty_entry import EmptyEntry
from automatic_warehouse.status_warehouse.entry.tray_entry import TrayEntry
from automatic_warehouse.status_warehouse.tray import Tray
from automatic_warehouse.warehouse import Warehouse


class TestGetMethodsCarousel(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.carousel_config = CarouselConfiguration(
            length=450,
            bay_height = 150,
            buffer_height = 150,
            x_offset = 125,
            width = 250,
            hole_height=150
        )
        self.carousel = Carousel(self.carousel_config, self.warehouse)

    def test_get_buffer(self):
        # arrange
        carousel = self.carousel

        # act
        buffer_get = carousel.get_buffer()
        buffer_expected = carousel.buffer

        # assert
        self.assertEqual(buffer_get, buffer_expected)

    def test_get_bay(self):
        # arrange
        carousel = self.carousel

        # act
        bay_get = carousel.get_bay()
        bay_expected = carousel.bay

        # assert
        self.assertEqual(bay_get, bay_expected)

    def test_get_hole(self):
        # arrange
        carousel = self.carousel

        # act
        hole_get = carousel.get_hole()
        hole_expected = carousel.hole

        # assert
        self.assertEqual(hole_get, hole_expected)

    def test_get_bay_entry(self):
        # arrange
        carousel = self.carousel

        # act
        bay_entry_get = carousel.get_bay_entry()
        bay_entry_expected = carousel.container[0]

        # assert
        self.assertEqual(bay_entry_get, bay_entry_expected)

    def test_get_bay_tray(self):
        # arrange
        bay_tray = Tray()
        carousel = self.carousel
        carousel.reset_container()
        carousel.add_tray(bay_tray)

        # act
        bay_tray_get = carousel.get_bay_tray()
        bay_tray_expected = bay_tray

        # assert
        self.assertEqual(bay_tray_get, bay_tray_expected)

    def test_get_buffer_entry(self):
        # arrange
        carousel = self.carousel

        # act
        buffer_entry_get = carousel.get_buffer_entry()
        buffer_entry_expected = carousel.container[1]

        # assert
        self.assertEqual(buffer_entry_get, buffer_entry_expected)

    def test_get_buffer_tray(self):
        # arrange
        bay_tray = Tray()
        buffer_tray = Tray()
        carousel = self.carousel
        carousel.reset_container()
        carousel.add_tray(bay_tray)
        carousel.add_tray(buffer_tray)

        # act
        buffer_tray_get = carousel.get_buffer_tray()
        buffer_tray_expected = buffer_tray

        # assert
        self.assertEqual(buffer_tray_get, buffer_tray_expected)

    def test_get_num_trays(self):
        # arrange
        carousel = self.carousel

        # act
        num_trays_get = carousel.get_num_trays()
        num_trays_expected = (isinstance(carousel.get_bay_entry(), TrayEntry) +
                                isinstance(carousel.get_buffer_entry(), TrayEntry))

        # assert
        self.assertEqual(num_trays_get, num_trays_expected)

    def test_get_num_entries_free(self):
        # arrange
        carousel = self.carousel

        # act
        num_entries_free_get = carousel.get_num_entries_free()
        num_entries_free_expected = sum(isinstance(entry, EmptyEntry) for entry in carousel.get_container())

        # assert
        self.assertEqual(num_entries_free_get, num_entries_free_expected)
