import copy
import unittest
import uuid

from src.sim.drawer import gen_rand_drawers, Drawer
from src.sim.material import gen_rand_material, Material, gen_rand_materials
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class TestDrawer(unittest.TestCase):
    def setUp(self):
        self.config = WarehouseConfigurationSingleton.get_instance()
        self.drawer = Drawer(gen_rand_materials(2))

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

    def test_get_items(self):
        # arrange
        drawer = self.drawer

        # act
        items_get = drawer.get_items()
        items_expected = drawer.items

        # assert
        self.assertEqual(items_get, items_expected)

    def test_get_max_height(self):
        # arrange
        drawer = self.drawer

        # act
        max_height_get = drawer.get_max_height()
        max_height_expected = drawer.max_height

        # assert
        self.assertEqual(max_height_get, max_height_expected)

    def test_get_num_space_occupied(self):
        # arrange
        drawer = self.drawer

        # act
        num_space_occupied_get = drawer.get_num_space_occupied()
        num_space_occupied_expected = drawer.num_space

        # assert
        self.assertEqual(num_space_occupied_get, num_space_occupied_expected)

    def test_get_first_drawerEntry(self):
        # arrange
        drawer = self.drawer

        # act
        first_drawerEntry_get = drawer.get_first_drawerEntry()
        first_drawerEntry_expected = drawer.first_drawerEntry

        # assert
        self.assertEqual(first_drawerEntry_get, first_drawerEntry_expected)

    def test_get_best_offset_x(self):
        # arrange
        drawer = self.drawer

        # act
        best_offset_x_get = drawer.get_best_offset_x()
        best_offset_x_expected = drawer.best_offset_x

        # assert
        self.assertEqual(best_offset_x_get, best_offset_x_expected)

    def test_get_best_y(self):
        # arrange
        drawer = self.drawer

        # act
        best_y_get = drawer.get_best_y()
        best_y_expected = drawer.best_y

        # assert
        self.assertEqual(best_y_get, best_y_expected)

    def test_get_num_materials(self):
        # arrange
        drawer = self.drawer

        # act
        num_materials_get = drawer.get_num_materials()
        num_materials_expected = len(drawer.items)

        # assert
        self.assertEqual(num_materials_get, num_materials_expected)

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
