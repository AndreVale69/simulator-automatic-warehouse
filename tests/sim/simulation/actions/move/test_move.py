from unittest import TestCase

import simpy

from src.simulation.actions.buffer import Buffer
from src.simulation.actions.move.move import Move
from src.simulation.simulation import Simulation
from src.warehouse import Warehouse


class TestMove(TestCase):
    def setUp(self):
        simulation = Simulation()
        warehouse = Warehouse()
        self.buffer = Buffer(simpy.Environment(), warehouse, simulation)
        self.move = Move(simulation.get_environment(), warehouse, simulation)

    def test_get_buffer(self):
        # arrange
        move = self.move

        # act
        self.move.buffer = self.buffer
        tray = move.get_buffer()

        # assert
        self.assertEqual(tray, self.buffer)
