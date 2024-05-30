import copy
from unittest import TestCase

from src.status_warehouse.container.carousel import Carousel, CarouselInfo
from src.warehouse import Warehouse


class TestBuiltinCarousel(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.carousel_config = CarouselInfo (
            bay_height = 150,
            buffer_height = 150,
            x_offset = 125,
            width = 250
        )
        self.carousel = Carousel(self.carousel_config, self.warehouse)

    def test_deepcopy(self):
        # arrange
        carousel = self.carousel

        # act
        deepcopy_carousel = copy.deepcopy(carousel)

        # assert
        self.assertIsInstance(deepcopy_carousel, Carousel)
        self.assertEqual(carousel, deepcopy_carousel)
        self.assertNotEqual(id(carousel), id(deepcopy_carousel))

    def test_eq(self):
        # arrange
        carousel = self.carousel

        # act

        # assert
        self.assertTrue(carousel.__eq__(carousel))

    def test_hash(self):
        # arrange
        carousel_1 = self.carousel
        carousel_2 = Carousel(
            CarouselInfo(
                bay_height=self.carousel_config.bay_height + 10,
                buffer_height=self.carousel_config.buffer_height + 10,
                x_offset=self.carousel_config.x_offset + 25,
                width=self.carousel_config.width + 10
            ),
            Warehouse())

        # act

        # assert
        self.assertEqual(hash(carousel_1), hash(carousel_1))
        self.assertNotEqual(hash(carousel_1), hash(carousel_2))
