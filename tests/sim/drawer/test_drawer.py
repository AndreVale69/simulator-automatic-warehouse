import uuid
from unittest import TestCase

from src.sim.drawer import gen_rand_drawers, Drawer
from src.sim.material import Material, gen_rand_materials
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class TestDrawer(TestCase):
    def setUp(self):
        self.config = WarehouseConfigurationSingleton.get_instance()
        self.drawer = Drawer(gen_rand_materials(2))

    def test_add_material(self):
        # arrange
        config = self.config.get_configuration()
        height_material = 150
        material_to_add = Material(
            barcode=uuid.uuid4().hex,
            name='NameMaterial',
            height=height_material,
            length=150,
            width=150
        )
        drawer = Drawer()
        self.assertEqual(drawer.get_max_height(), config['default_height_space'])

        # act
        drawer.add_material(material_to_add)

        # assert
        self.assertIn(material_to_add, drawer.get_items())
        self.assertEqual(drawer.get_max_height(), height_material)

    def test_remove_material(self):
        # arrange
        config = self.config.get_configuration()
        height_material = 150
        material_to_remove = Material(
            barcode=uuid.uuid4().hex,
            name='NameMaterial',
            height=height_material,
            length=150,
            width=150
        )
        drawer = Drawer([material_to_remove])
        self.assertEqual(drawer.get_max_height(), height_material)
        self.assertIn(material_to_remove, drawer.get_items())

        # act
        drawer.remove_material(material_to_remove)

        # assert
        self.assertNotIn(material_to_remove, drawer.get_items())
        self.assertEqual(drawer.get_max_height(), config['default_height_space'])

    def test_set_first_drawerEntry(self):
        # arrange
        drawer = self.drawer
        drawer_entry: DrawerEntry = drawer.get_first_drawerEntry()
        offset_x = 1000
        pos_y = 5

        # act
        drawer_entry_expected = DrawerEntry(offset_x, pos_y)
        drawer.set_first_drawerEntry(drawer_entry_expected)

        # assert
        self.assertNotEqual(drawer_entry, drawer_entry_expected)
        self.assertEqual(drawer.get_first_drawerEntry(), drawer_entry_expected)

    def test_set_best_offset_x(self):
        # arrange
        drawer = self.drawer
        best_offset_x = 1
        if drawer.get_best_offset_x() is not None:
            best_offset_x += drawer.get_best_offset_x()

        # act
        drawer.set_best_offset_x(best_offset_x)

        # assert
        self.assertEqual(drawer.get_best_offset_x(), best_offset_x)

    def test_set_best_y(self):
        # arrange
        drawer = self.drawer
        best_y = 1
        if drawer.get_best_y() is not None:
            best_y += drawer.get_best_y()

        # act
        drawer.set_best_y(best_y)

        # assert
        self.assertEqual(drawer.get_best_y(), best_y)

    def test_calculate_max_height(self):
        # arrange
        height_material = 50
        max_height_material = 140
        material = Material(
            barcode=uuid.uuid4().hex,
            name='NameMaterial',
            height=height_material,
            length=150,
            width=150
        )
        max_material = Material(
            barcode=uuid.uuid4().hex,
            name='NameMaterial',
            height=max_height_material,
            length=150,
            width=150
        )

        # act
        drawer = Drawer([material, max_material])

        # assert
        self.assertIn(material, drawer.get_items())
        self.assertIn(max_material, drawer.get_items())
        self.assertNotEqual(drawer.get_max_height(), height_material)
        self.assertEqual(drawer.get_max_height(), max_height_material)

    def test_random_drawers(self):
        # arrange
        max_height = 100
        min_height = 25
        drawers_to_generate = 5
        drawers_to_generate_less = 4
        materials_to_generate = 5
        materials_to_generate_less = 4
        materials_added = 0


        # act
        materials_generated = gen_rand_materials(materials_to_generate, min_height, max_height)
        materials_generated_less = gen_rand_materials(materials_to_generate_less, min_height, max_height)
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
