import copy
from unittest import TestCase
from unittest.mock import patch

from automatic_warehouse.status_warehouse.container.tray_container import TrayContainer
from automatic_warehouse.status_warehouse.entry.empty_entry import EmptyEntry
from automatic_warehouse.status_warehouse.entry.tray_entry import TrayEntry
from automatic_warehouse.warehouse import Warehouse


class TestTrayContainer(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.tray_container = self.warehouse.get_column(0)
        # use mock.patch to test abstract classes
        self.patch_tray_container = patch.multiple(TrayContainer, __abstractmethods__=set())
        self.patch_tray_container.start()

    def tearDown(self):
        self.patch_tray_container.stop()

    def test_set_warehouse(self):
        # arrange
        warehouse = self.warehouse
        new_warehouse = Warehouse()
        self.assertNotEqual(warehouse, new_warehouse)
        tray_container = self.tray_container

        # act
        self.assertEqual(tray_container.get_warehouse(), warehouse)
        tray_container.set_warehouse(new_warehouse)

        # assert
        self.assertEqual(tray_container.get_warehouse(), new_warehouse)

    def test_create_new_space(self):
        # arrange
        tray_container = self.tray_container
        container = copy.deepcopy(tray_container.get_container())
        empty_entry = EmptyEntry(200, 200)

        # act
        tray_container.create_new_space(empty_entry)

        # arrange
        self.assertNotEqual(container, tray_container.get_container())
        self.assertNotEqual(len(container), len(tray_container.get_container()))
        self.assertEqual(len(tray_container.get_container())-len(container), 1)

    def test_reset_container(self):
        # arrange
        tray_container = self.tray_container

        # act
        tray_container.reset_container()
        search_tray_entries = len([entry for entry in tray_container.get_container() if isinstance(entry, TrayEntry)])

        # assert
        self.assertEqual(search_tray_entries, 0)

    def test_is_full_abstractmethod(self):
        # arrange
        tray_container = TrayContainer(1000, 425, 200, 400, self.warehouse)

        # act

        # assert
        self.assertRaises(NotImplementedError, tray_container.is_full)

    def test_is_empty_abstractmethod(self):
        # arrange
        tray_container = TrayContainer(1000, 425, 200, 400, self.warehouse)

        # act

        # assert
        self.assertRaises(NotImplementedError, tray_container.is_empty)
