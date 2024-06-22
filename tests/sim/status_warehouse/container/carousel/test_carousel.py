from unittest import TestCase

from automatic_warehouse.status_warehouse.container.carousel import Carousel, CarouselConfiguration
from automatic_warehouse.status_warehouse.entry.tray_entry import TrayEntry
from automatic_warehouse.tray import Tray
from automatic_warehouse.warehouse import Warehouse
from automatic_warehouse.warehouse_configuration_singleton import TrayConfiguration, WarehouseConfigurationSingleton


class TestCarousel(TestCase):
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

    def test_carousel_info_parameter(self):
        # arrange
        param_1: int = 1
        param_2: str = 'str'
        param_3: float = 3.6
        param_4: int = 4
        param_5: float = 5.18
        param_6: float = 6.2

        # act

        # assert
        self.assertRaises(TypeError, CarouselConfiguration, **{
            'bay_height': param_1,
            'buffer_height': param_2,
            'x_offset': param_3,
            'width': param_4,
            'hole_height': param_5,
            'length' : param_6
        })

    def test_is_full(self):
        # arrange
        carousel = self.carousel

        # act
        is_full = carousel.is_full()
        expected_is_full = carousel.is_buffer_full() and carousel.is_bay_full()

        # assert
        self.assertEqual(is_full, expected_is_full)

    def test_is_empty(self):
        # arrange
        carousel = self.carousel

        # act
        is_empty = carousel.is_empty()
        expected_is_empty = not carousel.is_buffer_full() and not carousel.is_bay_full()

        # assert
        self.assertEqual(is_empty, expected_is_empty)

    def test_is_buffer_full(self):
        # arrange
        carousel = self.carousel

        # act
        is_buffer_full = carousel.is_buffer_full()
        expected_is_buffer_full = isinstance(carousel.get_buffer_entry(), TrayEntry)

        # assert
        self.assertEqual(is_buffer_full, expected_is_buffer_full)

    def test_is_bay_full(self):
        # arrange
        carousel = self.carousel

        # act
        is_bay_full = carousel.is_bay_full()
        expected_is_bay_full = isinstance(carousel.get_bay_entry(), TrayEntry)

        # assert
        self.assertEqual(is_bay_full, expected_is_bay_full)

    def test_add_tray(self):
        # arrange
        config = WarehouseConfigurationSingleton.get_instance().get_configuration()
        tray = Tray()
        warehouse = self.warehouse
        carousel = warehouse.get_carousel()

        # act
        carousel.reset_container()
        self.assertTrue(carousel.is_empty())
        carousel.add_tray(tray)

        # assert
        self.assertTrue(carousel.is_bay_full())
        self.assertFalse(carousel.is_buffer_full())
        self.assertRaises(ValueError, carousel.add_tray, Tray(TrayConfiguration(
            length=config.carousel.length,
            width=config.carousel.width,
            maximum_height=config.carousel.buffer_height
        )))

    def test_add_tray_full(self):
        # arrange
        tray_1 = Tray()
        tray_2 = Tray()
        warehouse = self.warehouse
        carousel = warehouse.get_carousel()

        # act
        carousel.reset_container()
        self.assertTrue(carousel.is_empty())
        carousel.add_tray(tray_1)
        carousel.add_tray(tray_2)

        # assert
        self.assertTrue(carousel.is_full())
        self.assertRaises(RuntimeError, carousel.add_tray, tray_1)

    def test_remove_tray(self):
        # arrange
        tray_1 = Tray()
        tray_2 = Tray()
        carousel = self.carousel
        carousel.reset_container()
        self.assertTrue(carousel.is_empty())
        carousel.add_tray(tray_1)
        carousel.add_tray(tray_2)
        self.assertTrue(carousel.is_bay_full())
        self.assertTrue(carousel.is_buffer_full())

        # act
        successful_remove_1 = carousel.remove_tray(tray_1)
        successful_remove_2 = carousel.remove_tray(tray_2)
        failure_remove = carousel.remove_tray(tray_1)

        # assert
        self.assertTrue(successful_remove_1)
        self.assertTrue(successful_remove_2)
        self.assertFalse(failure_remove)
