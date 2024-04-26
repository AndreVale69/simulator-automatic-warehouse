import unittest
import copy

from src.sim.material import gen_rand_material, Material, gen_rand_materials


class TestMaterial(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_random_material(self):
        # arrange
        max_height = 100
        minimum_height = 25
        materials_to_generate = 5

        # act
        material_generated = gen_rand_material(max_height)
        materials = gen_rand_materials(materials_to_generate, max_height)

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

    def test_deepcopy(self):
        # arrange
        material: Material = gen_rand_material()

        # act
        deepcopy_material = copy.deepcopy(material)

        # assert
        self.assertIsInstance(deepcopy_material, Material)
        self.assertEqual(material, deepcopy_material)
        self.assertNotEqual(id(material), id(deepcopy_material))
