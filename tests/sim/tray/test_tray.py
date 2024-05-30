import uuid
from unittest import TestCase

from src.sim.tray import gen_rand_trays, Tray
from src.sim.material import Material, gen_rand_materials
from src.sim.status_warehouse.entry.tray_entry import TrayEntry
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class TestTray(TestCase):
    def setUp(self):
        self.config = WarehouseConfigurationSingleton.get_instance()
        self.tray = Tray(gen_rand_materials(2))

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
        tray = Tray()
        self.assertEqual(tray.get_max_height(), config['default_height_space'])

        # act
        tray.add_material(material_to_add)

        # assert
        self.assertIn(material_to_add, tray.get_items())
        self.assertEqual(tray.get_max_height(), height_material)

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
        tray = Tray([material_to_remove])
        self.assertEqual(tray.get_max_height(), height_material)
        self.assertIn(material_to_remove, tray.get_items())

        # act
        tray.remove_material(material_to_remove)

        # assert
        self.assertNotIn(material_to_remove, tray.get_items())
        self.assertEqual(tray.get_max_height(), config['default_height_space'])

    def test_set_first_trayEntry(self):
        # arrange
        tray = self.tray
        tray_entry: TrayEntry = tray.get_first_trayEntry()
        offset_x = 1000
        pos_y = 5

        # act
        tray_entry_expected = TrayEntry(offset_x, pos_y)
        tray.set_first_trayEntry(tray_entry_expected)

        # assert
        self.assertNotEqual(tray_entry, tray_entry_expected)
        self.assertEqual(tray.get_first_trayEntry(), tray_entry_expected)

    def test_set_best_offset_x(self):
        # arrange
        tray = self.tray
        best_offset_x = 1
        if tray.get_best_offset_x() is not None:
            best_offset_x += tray.get_best_offset_x()

        # act
        tray.set_best_offset_x(best_offset_x)

        # assert
        self.assertEqual(tray.get_best_offset_x(), best_offset_x)

    def test_set_best_y(self):
        # arrange
        tray = self.tray
        best_y = 1
        if tray.get_best_y() is not None:
            best_y += tray.get_best_y()

        # act
        tray.set_best_y(best_y)

        # assert
        self.assertEqual(tray.get_best_y(), best_y)

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
        tray = Tray([material, max_material])

        # assert
        self.assertIn(material, tray.get_items())
        self.assertIn(max_material, tray.get_items())
        self.assertNotEqual(tray.get_max_height(), height_material)
        self.assertEqual(tray.get_max_height(), max_height_material)

    def test_random_trays(self):
        # arrange
        max_height = 100
        min_height = 25
        trays_to_generate = 5
        trays_to_generate_less = 4
        materials_to_generate = 5
        materials_to_generate_less = 4
        materials_added = 0


        # act
        materials_generated = gen_rand_materials(materials_to_generate, min_height, max_height)
        materials_generated_less = gen_rand_materials(materials_to_generate_less, min_height, max_height)
        trays_generated = gen_rand_trays(trays_to_generate, materials_generated)
        trays_generated_less = gen_rand_trays(trays_to_generate_less, materials_generated)
        trays_generated_grater = gen_rand_trays(trays_to_generate, materials_generated_less)


        # assert
        self.assertEqual(len(trays_generated), trays_to_generate)
        self.assertEqual(len(trays_generated_less), trays_to_generate_less)
        self.assertEqual(len(trays_generated_grater), trays_to_generate)

        for tray in trays_generated:
            self.assertIsInstance(tray, Tray)
            materials_added += len(tray.get_items())
        self.assertEqual(materials_added, len(materials_generated))

        materials_added = 0
        for tray in trays_generated_less:
            self.assertIsInstance(tray, Tray)
            materials_added += len(tray.get_items())
        self.assertEqual(materials_added, len(materials_generated))

        materials_added = 0
        for tray in trays_generated_grater:
            self.assertIsInstance(tray, Tray)
            materials_added += len(tray.get_items())
        self.assertEqual(materials_added, len(materials_generated_less))
