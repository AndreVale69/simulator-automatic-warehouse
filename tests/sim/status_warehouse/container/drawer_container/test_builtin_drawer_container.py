from unittest import TestCase

from src.sim.status_warehouse.container.column import Column, ColumnInfo
from src.sim.status_warehouse.container.drawer_container import DrawerContainer
from src.sim.warehouse import Warehouse


class TestBuiltinDrawerContainer(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.get_column(0).gen_materials_and_drawers(6, 10)
        self.drawer_container = self.warehouse.get_column(0)

    def test_get_num_entries_free_abstractmethod(self):
        # arrange
        drawer_container = DrawerContainer(1025, 200, 400, Warehouse())

        # act

        # assert
        self.assertRaises(NotImplementedError, drawer_container.get_num_entries_free)

    def test_is_full_abstractmethod(self):
        # arrange
        drawer_container = DrawerContainer(1025, 200, 400, Warehouse())

        # act

        # assert
        self.assertRaises(NotImplementedError, drawer_container.is_full)

    def test_is_empty_abstractmethod(self):
        # arrange
        drawer_container = DrawerContainer(1025, 200, 400, Warehouse())

        # act

        # assert
        self.assertRaises(NotImplementedError, drawer_container.is_empty)


    def test_eq(self):
        # arrange
        drawer_container = self.drawer_container

        # act

        # assert
        self.assertTrue(drawer_container.__eq__(drawer_container))

    def test_hash(self):
        # arrange
        drawer_container_1 = self.drawer_container
        drawer_container_2 = Column(ColumnInfo(
            height = 5 * 25,
            x_offset = 150,
            width = 200,
            height_last_position = 50
        ), self.warehouse)

        # act

        # assert
        self.assertEqual(hash(drawer_container_1), hash(drawer_container_1))
        self.assertNotEqual(hash(drawer_container_1), hash(drawer_container_2))
