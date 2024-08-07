from unittest import TestCase
from unittest.mock import patch

import simpy

from automatic_warehouse.simulation.actions.buffer import Buffer
from automatic_warehouse.simulation.actions.move.move import Move
from automatic_warehouse.simulation.simulation import Simulation
from automatic_warehouse.warehouse import Warehouse


class TestMove(TestCase):
    def setUp(self):
        # use mock.patch to test abstract classes
        self.patch_simulation = patch.multiple(Simulation, __abstractmethods__=set())
        self.patch_simulation.start()
        simulation = Simulation()
        warehouse = Warehouse()
        self.buffer = Buffer(simpy.Environment(), warehouse, simulation)
        self.move = Move(simulation.get_environment(), warehouse, simulation)

    def tearDown(self):
        self.patch_simulation.stop()

    def test_get_buffer(self):
        # arrange
        move = self.move

        # act
        self.move.buffer = self.buffer
        tray = move.get_buffer()

        # assert
        self.assertEqual(tray, self.buffer)

    def test_simulate_action_abstractmethod(self):
        # arrange
        move = self.move

        # act

        # assert
        self.assertRaises(NotImplementedError, move.simulate_action)
