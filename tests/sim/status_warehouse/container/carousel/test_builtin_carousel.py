import copy
import unittest

from src.sim.warehouse import Warehouse
from src.sim.status_warehouse.container.carousel import Carousel


class TestBuiltinCarousel(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.carousel_config = {
            "deposit_height": 150,
            "buffer_height": 150,
            "x_offset": 125,
            "width": 250
        }
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
        carousel_2 = Carousel({
            "deposit_height": 160,
            "buffer_height": 160,
            "x_offset": 150,
            "width": 260
        }, Warehouse())

        # act

        # assert
        self.assertEqual(hash(carousel_1), hash(carousel_1))
        self.assertNotEqual(hash(carousel_1), hash(carousel_2))
