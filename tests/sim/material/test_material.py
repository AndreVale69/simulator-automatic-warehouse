import uuid
from unittest import TestCase

from src.material import gen_rand_material, Material, gen_rand_materials
from src.warehouse_configuration_singleton import WarehouseConfigurationSingleton, CarouselConfiguration


class TestMaterial(TestCase):
    def test_material_too_high(self):
        # arrange
        config: CarouselConfiguration = WarehouseConfigurationSingleton.get_instance().get_configuration().carousel
        max_height_material = config.buffer_height

        # act

        # assert
        self.assertRaises(ValueError, Material, uuid.uuid4().hex, 'name', max_height_material+1, 100, 100)

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
