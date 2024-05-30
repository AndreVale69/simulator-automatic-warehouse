from unittest import TestCase

from src.sim.tray import Tray
from src.sim.status_warehouse.container.carousel import Carousel, CarouselInfo
from src.sim.status_warehouse.entry.tray_entry import TrayEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.warehouse import Warehouse


class TestGetMethodsCarousel(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.carousel_config = CarouselInfo (
            deposit_height = 150,
            buffer_height = 150,
            x_offset = 125,
            width = 250
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

    def test_get_deposit_tray(self):
        # arrange
        deposit_tray = Tray()
        carousel = self.carousel
        carousel.reset_container()
        carousel.add_tray(deposit_tray)

        # act
        deposit_tray_get = carousel.get_deposit_tray()
        deposit_tray_expected = deposit_tray

        # assert
        self.assertEqual(deposit_tray_get, deposit_tray_expected)

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
        deposit_tray = Tray()
        buffer_tray = Tray()
        carousel = self.carousel
        carousel.reset_container()
        carousel.add_tray(deposit_tray)
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
        num_trays_expected = (isinstance(carousel.get_deposit_entry(), TrayEntry) +
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
