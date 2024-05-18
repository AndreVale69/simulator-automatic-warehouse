from unittest import TestCase

from src.sim.drawer import Drawer
from src.sim.material import gen_rand_material
from src.sim.simulation.actions.move.move import Move
from src.sim.simulation.simulation import Simulation
from src.sim.status_warehouse.enum_warehouse import EnumWarehouse
from src.sim.warehouse import Warehouse


class TestMove(TestCase):
    def setUp(self):
        simulation = Simulation()
        self.drawer = Drawer()
        self.move = Move(simulation.get_environment(), Warehouse(), simulation, EnumWarehouse.CAROUSEL, self.drawer)

    def test_set_drawer(self):
        # arrange
        move = self.move
        drawer = Drawer([gen_rand_material()])

        # act
        move.set_drawer(drawer)

        # assert
        self.assertEqual(drawer, move.get_drawer())

    def test_get_drawer(self):
        # arrange
        move = self.move

        # act
        drawer = move.get_drawer()

        # assert
        self.assertEqual(drawer, self.drawer)