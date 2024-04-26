import unittest
import copy

from src.sim.material import gen_rand_material, Material, gen_rand_materials
from src.sim.drawer import gen_rand_drawers, Drawer


class TestDrawer(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_random_drawers(self):
        # arrange
        max_height = 100
        drawers_to_generate = 5
        drawers_to_generate_less = 4
        materials_to_generate = 5
        materials_to_generate_less = 4
        materials_added = 0

        # act
        materials_generated = gen_rand_materials(materials_to_generate, max_height)
        materials_generated_less = gen_rand_materials(materials_to_generate_less, max_height)
        drawers_generated = gen_rand_drawers(drawers_to_generate, materials_generated)
        drawers_generated_less = gen_rand_drawers(drawers_to_generate_less, materials_generated)
        drawers_generated_grater = gen_rand_drawers(drawers_to_generate, materials_generated_less)


        # assert
        self.assertEqual(len(drawers_generated), drawers_to_generate)
        self.assertEqual(len(drawers_generated_less), drawers_to_generate_less)
        self.assertEqual(len(drawers_generated_grater), drawers_to_generate)

        for drawer in drawers_generated:
            self.assertIsInstance(drawer, Drawer)
            materials_added += len(drawer.get_items())
        self.assertEqual(materials_added, len(materials_generated))

        materials_added = 0
        for drawer in drawers_generated_less:
            self.assertIsInstance(drawer, Drawer)
            materials_added += len(drawer.get_items())
        self.assertEqual(materials_added, len(materials_generated))

        materials_added = 0
        for drawer in drawers_generated_grater:
            self.assertIsInstance(drawer, Drawer)
            materials_added += len(drawer.get_items())
        self.assertEqual(materials_added, len(materials_generated_less))


    def test_deepcopy(self):
        # arrange
        drawer: Drawer = gen_rand_drawers(1, [gen_rand_material(100)])[0]

        # act
        deepcopy_drawer = copy.deepcopy(drawer)

        # assert
        self.assertIsInstance(deepcopy_drawer, Drawer)
        self.assertEqual(drawer, deepcopy_drawer)
