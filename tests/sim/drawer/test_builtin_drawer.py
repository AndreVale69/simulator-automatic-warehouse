import copy
import unittest
import uuid

from src.sim.drawer import gen_rand_drawers, Drawer
from src.sim.material import gen_rand_material, Material


class TestBuiltinDrawer(unittest.TestCase):
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
        drawer_1 = Drawer([mat_1, mat_2])
        drawer_2 = Drawer([mat_1, mat_2])
        drawer_3 = Drawer([mat_1, mat_2, mat_3])

        # act

        # assert
        self.assertNotEqual(id(drawer_1), id(drawer_2))
        self.assertEqual(drawer_1, drawer_2)
        self.assertNotEqual(drawer_1, drawer_3)

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
        drawer_1 = Drawer([mat_1, mat_2])
        drawer_2 = Drawer([mat_1, mat_2])
        drawer_3 = Drawer([mat_1, mat_2, mat_3])

        # act

        # assert
        self.assertNotEqual(id(drawer_1), id(drawer_2))
        self.assertEqual(drawer_1, drawer_2)
        self.assertNotEqual(drawer_1, drawer_3)
        self.assertEqual(hash(drawer_1), hash(drawer_1))
        self.assertEqual(hash(drawer_1), hash(drawer_2))
        self.assertNotEqual(hash(drawer_1), hash(drawer_3))

    def test_deepcopy(self):
        # arrange
        drawer: Drawer = gen_rand_drawers(1, [gen_rand_material(max_height=100)])[0]

        # act
        deepcopy_drawer = copy.deepcopy(drawer)

        # assert
        self.assertIsInstance(deepcopy_drawer, Drawer)
        self.assertEqual(drawer, deepcopy_drawer)
        self.assertNotEqual(id(drawer), id(deepcopy_drawer))
