from unittest import TestCase

from automatic_warehouse.status_warehouse.entry.tray_entry import TrayEntry
from automatic_warehouse.warehouse import Warehouse


class TestGetMethodsTrayContainer(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.get_column(0).gen_materials_and_trays(6, 10)
        self.tray_container = self.warehouse.get_column(0)

    def test_get_warehouse(self):
        # arrange
        tray_container = self.tray_container

        # act
        warehouse_get = tray_container.get_warehouse()
        warehouse_expected = self.warehouse

        # assert
        self.assertEqual(warehouse_expected, warehouse_get)

    def test_get_height_warehouse(self):
        # arrange
        tray_container = self.tray_container

        # act
        height_warehouse_get = tray_container.get_height_warehouse()
        height_warehouse_expected = tray_container.height_warehouse

        # assert
        self.assertEqual(height_warehouse_expected, height_warehouse_get)

    def test_get_def_space(self):
        # arrange
        tray_container = self.tray_container

        # act
        def_space_get = tray_container.get_def_space()
        def_space_expected = tray_container.def_space

        # assert
        self.assertEqual(def_space_expected, def_space_get)

    def test_get_container(self):
        # arrange
        tray_container = self.tray_container

        # act
        container_get = tray_container.get_container()
        container_expected = tray_container.container

        # assert
        self.assertEqual(container_expected, container_get)

    def test_get_offset_x(self):
        # arrange
        tray_container = self.tray_container

        # act
        offset_x_get = tray_container.get_offset_x()
        offset_x_expected = tray_container.offset_x

        # assert
        self.assertEqual(offset_x_expected, offset_x_get)

    def test_get_height_container(self):
        # arrange
        tray_container = self.tray_container

        # act
        height_container_get = tray_container.get_height_container()
        height_container_expected = tray_container.height_container

        # assert
        self.assertEqual(height_container_expected, height_container_get)

    def test_get_num_entries(self):
        # arrange
        tray_container = self.tray_container

        # act
        num_entries_get = tray_container.get_num_entries()
        num_entries_expected = tray_container.num_entries

        # assert
        self.assertEqual(num_entries_expected, num_entries_get)

    def test_get_width(self):
        # arrange
        tray_container = self.tray_container

        # act
        width_get = tray_container.get_width()
        width_expected = tray_container.width

        # assert
        self.assertEqual(width_expected, width_get)

    def test_get_length(self):
        # arrange
        tray_container = self.tray_container

        # act
        length_get = tray_container.get_length()
        length_expected = tray_container.length

        # assert
        self.assertEqual(length_expected, length_get)

    def test_get_num_trays(self):
        # arrange
        tray_container = self.tray_container

        # act
        num_trays_get = tray_container.get_num_trays()
        num_trays_expected = {entry.get_tray() for entry in tray_container.get_container() if isinstance(entry, TrayEntry)}

        # assert
        self.assertEqual(len(num_trays_expected), num_trays_get)

    def test_get_num_entries_occupied(self):
        # arrange
        tray_container = self.tray_container

        # act
        num_entries_occupied_get = tray_container.get_num_entries_occupied()
        num_entries_occupied_expected = len([entry for entry in tray_container.get_container() if isinstance(entry, TrayEntry)])

        # assert
        self.assertEqual(num_entries_occupied_expected, num_entries_occupied_get)

    def test_get_trays(self):
        # arrange
        tray_container = self.tray_container

        # act
        trays_get = set(tray_container.get_trays())
        trays_expected = {entry.get_tray() for entry in tray_container.get_container() if isinstance(entry, TrayEntry)}

        # assert
        self.assertSetEqual(trays_expected, trays_get)

    def test_get_entries_occupied(self):
        # arrange
        tray_container = self.tray_container

        # act
        entries_occupied_get = tray_container.get_entries_occupied()
        entries_occupied_expected = [entry for entry in tray_container.get_container() if isinstance(entry, TrayEntry)]

        # assert
        self.assertEqual(entries_occupied_expected, entries_occupied_get)

    def test_get_num_materials(self):
        # arrange
        tray_container = self.tray_container

        # act
        num_materials_get = tray_container.get_num_materials()
        num_materials_expected = sum(tray.get_num_materials() for tray in tray_container.get_trays())

        # assert
        self.assertEqual(num_materials_expected, num_materials_get)
