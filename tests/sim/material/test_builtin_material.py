import copy
import uuid
from unittest import TestCase

from src.material import gen_rand_material, Material


class TestBuiltinMaterial(TestCase):
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
