from unittest import TestCase

from src.sim.status_warehouse.container.drawer_container import DrawerContainer
from src.sim.warehouse import Warehouse


class TestBuiltinDrawerContainer(TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.get_column(0).gen_materials_and_drawers(6, 10)
        self.drawer_container = self.warehouse.get_column(0)

    def test_eq(self):
        # arrange
        drawer_container = self.drawer_container

        # act

        # assert
        self.assertTrue(drawer_container.__eq__(drawer_container))

    def test_hash(self):
        # arrange
        drawer_container_1 = self.drawer_container
        drawer_container_2 = DrawerContainer(1025, 200, 400, Warehouse())

        # act

        # assert
        self.assertEqual(hash(drawer_container_1), hash(drawer_container_1))
        self.assertNotEqual(hash(drawer_container_1), hash(drawer_container_2))
