from unittest import TestCase

from status_warehouse.material import gen_rand_material


class TestGetMethodsMaterial(TestCase):
    def setUp(self):
        self.material = gen_rand_material()

    def test_get_barcode(self):
        # arrange
        material = self.material

        # act
        barcode_get = material.get_barcode()
        barcode_expected = material.barcode

        # assert
        self.assertEqual(barcode_get, barcode_expected)

    def test_get_name(self):
        # arrange
        material = self.material

        # act
        name_get = material.get_name()
        name_expected = material.name

        # assert
        self.assertEqual(name_get, name_expected)

    def test_get_height(self):
        # arrange
        material = self.material

        # act
        height_get = material.get_height()
        height_expected = material.height

        # assert
        self.assertEqual(height_get, height_expected)

    def test_get_length(self):
        # arrange
        material = self.material

        # act
        length_get = material.get_length()
        length_expected = material.length

        # assert
        self.assertEqual(length_get, length_expected)

    def test_get_width(self):
        # arrange
        material = self.material

        # act
        width_get = material.get_width()
        width_expected = material.width

        # assert
        self.assertEqual(width_get, width_expected)
