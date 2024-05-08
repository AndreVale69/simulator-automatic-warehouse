from unittest import TestCase

from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.warehouse import Warehouse


class TestGetMethodsDrawerContainer(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.get_column(0).gen_materials_and_drawers(6, 10)
        self.drawer_container = self.warehouse.get_column(0)

    def test_get_warehouse(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        warehouse_get = drawer_container.get_warehouse()
        warehouse_expected = self.warehouse

        # assert
        self.assertEqual(warehouse_expected, warehouse_get)

    def test_get_height_warehouse(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        height_warehouse_get = drawer_container.get_height_warehouse()
        height_warehouse_expected = drawer_container.height_warehouse

        # assert
        self.assertEqual(height_warehouse_expected, height_warehouse_get)

    def test_get_def_space(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        def_space_get = drawer_container.get_def_space()
        def_space_expected = drawer_container.def_space

        # assert
        self.assertEqual(def_space_expected, def_space_get)

    def test_get_container(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        container_get = drawer_container.get_container()
        container_expected = drawer_container.container

        # assert
        self.assertEqual(container_expected, container_get)

    def test_get_offset_x(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        offset_x_get = drawer_container.get_offset_x()
        offset_x_expected = drawer_container.offset_x

        # assert
        self.assertEqual(offset_x_expected, offset_x_get)

    def test_get_height_container(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        height_container_get = drawer_container.get_height_container()
        height_container_expected = drawer_container.height_container

        # assert
        self.assertEqual(height_container_expected, height_container_get)

    def test_get_width(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        width_get = drawer_container.get_width()
        width_expected = drawer_container.width

        # assert
        self.assertEqual(width_expected, width_get)

    def test_get_num_drawers(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        num_drawers_get = drawer_container.get_num_drawers()
        num_drawers_expected = {entry.get_drawer() for entry in drawer_container.get_container() if isinstance(entry, DrawerEntry)}

        # assert
        self.assertEqual(len(num_drawers_expected), num_drawers_get)

    def test_get_num_entries_occupied(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        num_entries_occupied_get = drawer_container.get_num_entries_occupied()
        num_entries_occupied_expected = len([entry for entry in drawer_container.get_container() if isinstance(entry, DrawerEntry)])

        # assert
        self.assertEqual(num_entries_occupied_expected, num_entries_occupied_get)

    def test_get_drawers(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        drawers_get = set(drawer_container.get_drawers())
        drawers_expected = {entry.get_drawer() for entry in drawer_container.get_container() if isinstance(entry, DrawerEntry)}

        # assert
        self.assertSetEqual(drawers_expected, drawers_get)

    def test_get_entries_occupied(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        entries_occupied_get = drawer_container.get_entries_occupied()
        entries_occupied_expected = [entry for entry in drawer_container.get_container() if isinstance(entry, DrawerEntry)]

        # assert
        self.assertEqual(entries_occupied_expected, entries_occupied_get)

    def test_get_num_materials(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        num_materials_get = drawer_container.get_num_materials()
        num_materials_expected = sum(drawer.get_num_materials() for drawer in drawer_container.get_drawers())

        # assert
        self.assertEqual(num_materials_expected, num_materials_get)
