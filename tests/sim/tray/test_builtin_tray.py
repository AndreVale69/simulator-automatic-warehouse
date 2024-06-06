import copy
import uuid
from unittest import TestCase

from src.material import gen_rand_material, Material
from src.tray import gen_rand_trays, Tray


class TestBuiltinTray(TestCase):
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
        tray_1 = Tray([mat_1, mat_2])
        tray_2 = Tray([mat_1, mat_2])
        tray_3 = Tray([mat_1, mat_2, mat_3])

        # act

        # assert
        self.assertNotEqual(id(tray_1), id(tray_2))
        self.assertEqual(tray_1, tray_2)
        self.assertNotEqual(tray_1, tray_3)

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
        tray_1 = Tray([mat_1, mat_2])
        tray_2 = Tray([mat_1, mat_2])
        tray_3 = Tray([mat_1, mat_2, mat_3])

        # act

        # assert
        self.assertNotEqual(id(tray_1), id(tray_2))
        self.assertEqual(tray_1, tray_2)
        self.assertNotEqual(tray_1, tray_3)
        self.assertEqual(hash(tray_1), hash(tray_1))
        self.assertEqual(hash(tray_1), hash(tray_2))
        self.assertNotEqual(hash(tray_1), hash(tray_3))

    def test_deepcopy(self):
        # arrange
        tray: Tray = gen_rand_trays(1, [gen_rand_material(max_height=100)])[0]

        # act
        deepcopy_tray = copy.deepcopy(tray)

        # assert
        self.assertIsInstance(deepcopy_tray, Tray)
        self.assertEqual(tray, deepcopy_tray)
        self.assertNotEqual(id(tray), id(deepcopy_tray))
