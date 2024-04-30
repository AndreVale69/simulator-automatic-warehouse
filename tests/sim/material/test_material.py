import unittest

from src.sim.material import gen_rand_material, Material, gen_rand_materials


class TestMaterial(unittest.TestCase):
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
