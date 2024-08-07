from unittest import TestCase
from unittest.mock import patch

from automatic_warehouse.status_warehouse.container.column import Column
from automatic_warehouse.status_warehouse.container.tray_container import TrayContainer
from automatic_warehouse.warehouse import Warehouse
from automatic_warehouse.warehouse_configuration_singleton import ColumnConfiguration


class TestBuiltinTrayContainer(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.get_column(0).gen_materials_and_trays(6, 10)
        self.tray_container = self.warehouse.get_column(0)
        # use mock.patch to test abstract classes
        self.patch_tray_container = patch.multiple(TrayContainer, __abstractmethods__=set())
        self.patch_tray_container.start()

    def tearDown(self):
        self.patch_tray_container.stop()

    def test_get_num_entries_free_abstractmethod(self):
        # arrange
        tray_container = TrayContainer(1025, 200, 400, 400, Warehouse())

        # act

        # assert
        self.assertRaises(NotImplementedError, tray_container.get_num_entries_free)

    def test_is_full_abstractmethod(self):
        # arrange
        tray_container = TrayContainer(1025, 200, 400, 400, Warehouse())

        # act

        # assert
        self.assertRaises(NotImplementedError, tray_container.is_full)

    def test_is_empty_abstractmethod(self):
        # arrange
        tray_container = TrayContainer(1025, 200, 400, 400, Warehouse())

        # act

        # assert
        self.assertRaises(NotImplementedError, tray_container.is_empty)


    def test_eq(self):
        # arrange
        tray_container = self.tray_container

        # act

        # assert
        self.assertTrue(tray_container.__eq__(tray_container))

    def test_hash(self):
        # arrange
        tray_container_1 = self.tray_container
        tray_container_2 = Column(ColumnConfiguration(
            length=200,
            height = 5 * 25,
            x_offset = 150,
            width = 200,
            height_last_position = 50
        ), self.warehouse)

        # act

        # assert
        self.assertEqual(hash(tray_container_1), hash(tray_container_1))
        self.assertNotEqual(hash(tray_container_1), hash(tray_container_2))
