import unittest

from src.sim.status_warehouse.container.drawer_container import DrawerContainer
from src.sim.warehouse import Warehouse


class TestBuiltinDrawerContainer(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.drawer_container = DrawerContainer(1000, 125, 200, self.warehouse)

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
