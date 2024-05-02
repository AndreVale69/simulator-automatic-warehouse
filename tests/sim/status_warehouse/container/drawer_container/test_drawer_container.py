import copy
import unittest

from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry
from src.sim.warehouse import Warehouse


class TestDrawerContainer(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.drawer_container = self.warehouse.get_column(0)

    def test_set_warehouse(self):
        # arrange
        warehouse = self.warehouse
        new_warehouse = Warehouse()
        self.assertNotEqual(warehouse, new_warehouse)
        drawer_container = self.drawer_container

        # act
        self.assertEqual(drawer_container.get_warehouse(), warehouse)
        drawer_container.set_warehouse(new_warehouse)

        # assert
        self.assertEqual(drawer_container.get_warehouse(), new_warehouse)

    def test_create_new_space(self):
        # arrange
        drawer_container = self.drawer_container
        container = copy.deepcopy(drawer_container.get_container())
        empty_entry = EmptyEntry(200, 200)

        # act
        drawer_container.create_new_space(empty_entry)

        # arrange
        self.assertNotEqual(container, drawer_container.get_container())
        self.assertNotEqual(len(container), len(drawer_container.get_container()))
        self.assertEqual(len(drawer_container.get_container())-len(container), 1)

    def test_reset_container(self):
        # arrange
        drawer_container = self.drawer_container

        # act
        drawer_container.reset_container()
        search_drawer_entries = len([entry for entry in drawer_container.get_container() if isinstance(entry, DrawerEntry)])

        # assert
        self.assertEqual(search_drawer_entries, 0)
