from unittest import TestCase
from unittest.mock import patch

from simpy import Environment

from automatic_warehouse.simulation.actions.action import Action
from automatic_warehouse.warehouse import Warehouse


class TestAction(TestCase):
    def setUp(self):
        self.env = Environment()
        self.warehouse = Warehouse()
        # use mock.patch to test abstract classes
        self.patch_action = patch.multiple(Action, __abstractmethods__=set())
        self.patch_action.start()
        self.action = Action(self.env, self.warehouse, None)

    def tearDown(self):
        self.patch_action.stop()

    def test_get_env(self):
        # arrange
        env = self.env

        # act
        actual_env = self.action.get_env()

        # assert
        self.assertEqual(actual_env, env)

    def test_get_warehouse(self):
        # arrange
        warehouse = self.warehouse

        # act
        actual_warehouse = self.action.get_warehouse()

        # assert
        self.assertEqual(actual_warehouse, warehouse)

    def test_get_simulation(self):
        # arrange

        # act
        actual_simulation = self.action.get_simulation()

        # assert
        self.assertIsNone(actual_simulation)

    def test_simulate_action_abstractmethod(self):
        # arrange
        action = self.action

        # act

        # assert
        self.assertRaises(NotImplementedError, action.simulate_action)