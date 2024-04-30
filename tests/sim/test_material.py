import copy
import unittest
import uuid

from src.sim.material import gen_rand_material, Material, gen_rand_materials


class TestMaterial(unittest.TestCase):
    def setUp(self):
        self.material = gen_rand_material()

    def test_eq(self):
        # arrange
        hex_material = uuid.uuid4().hex
        mat_1 = Material(barcode=hex_material,
                         name='material_name',
                         height=100,
                         length=100,
                         width=100)
        mat_2 = Material(barcode=hex_material,
                         name='material_name',
                         height=100,
                         length=100,
                         width=100)
        mat_3 = Material(barcode=uuid.uuid4().hex,
                         name='different_name',
                         height=50,
                         length=50,
                         width=50)

        # act

        # assert
        self.assertNotEqual(id(mat_1), id(mat_2))
        self.assertEqual(mat_1, mat_2)
        self.assertNotEqual(mat_1, mat_3)

    def test_hash(self):
        # arrange
        hex_material = uuid.uuid4().hex
        mat_1 = Material(barcode=hex_material,
                         name='material_name',
                         height=100,
                         length=100,
                         width=100)
        mat_2 = Material(barcode=hex_material,
                         name='material_name',
                         height=100,
                         length=100,
                         width=100)
        mat_3 = Material(barcode=uuid.uuid4().hex,
                         name='different_name',
                         height=50,
                         length=50,
                         width=50)

        # act

        # assert
        self.assertNotEqual(id(mat_1), id(mat_2))
        self.assertEqual(mat_1, mat_2)
        self.assertNotEqual(mat_1, mat_3)
        self.assertEqual(hash(mat_1), hash(mat_1))
        self.assertEqual(hash(mat_1), hash(mat_2))
        self.assertNotEqual(hash(mat_1), hash(mat_3))

    def test_deepcopy(self):
        # arrange
        material: Material = gen_rand_material()

        # act
        deepcopy_material = copy.deepcopy(material)

        # assert
        self.assertIsInstance(deepcopy_material, Material)
        self.assertEqual(material, deepcopy_material)
        self.assertNotEqual(id(material), id(deepcopy_material))

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

    def test_gen_rand_material_and_materials(self):
        # arrange
        max_height = 100
        minimum_height = 25
        materials_to_generate = 5

        # act
        material_generated = gen_rand_material(min_height=minimum_height, max_height=max_height)
        materials = gen_rand_materials(materials_to_generate, minimum_height, max_height)

        # assert
        # single material
        self.assertIsInstance(material_generated, Material)
        self.assertLessEqual(material_generated.get_height(), max_height)
        self.assertGreaterEqual(material_generated.get_height(), minimum_height)
        # multiple materials
        self.assertEqual(len(materials), materials_to_generate)
        for material in materials:
            self.assertIsInstance(material, Material)
            self.assertLessEqual(material.get_height(), max_height)
            self.assertGreaterEqual(material.get_height(), minimum_height)
