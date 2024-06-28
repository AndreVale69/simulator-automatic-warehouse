from unittest import TestCase
from unittest.mock import patch

from pandas import DataFrame

from automatic_warehouse.simulation.simulation import Simulation


class TestSimulation(TestCase):
    def setUp(self):
        # use mock.patch to test abstract classes
        self.patch_simulation = patch.multiple(Simulation, __abstractmethods__=set())
        self.patch_simulation.start()
        self.simulation = Simulation()

    def tearDown(self):
        self.patch_simulation.stop()

    def test_eq(self):
        # arrange
        simulation = self.simulation

        # act

        # assert
        self.assertTrue(simulation.__eq__(simulation))

    def test_get_environment(self):
        # arrange
        simulation = self.simulation

        # act
        env_get = simulation.get_environment()
        env_expected = simulation.env

        # assert
        self.assertEqual(env_get, env_expected)

    def test_get_store_history(self):
        # arrange
        simulation = self.simulation

        # act
        store_history_get = simulation.get_store_history()
        store_history_expected = simulation.store_history

        # assert
        self.assertEqual(store_history_get, store_history_expected)

    def test_get_store_history_dataframe(self):
        # arrange
        simulation = self.simulation

        # act

        # assert
        self.assertIsInstance(simulation.get_store_history_dataframe(), DataFrame)

    def test_get_sim_time(self):
        # arrange
        simulation = self.simulation

        # act
        sim_time_get = simulation.get_sim_time()
        sim_time_expected = simulation.sim_time

        # assert
        self.assertEqual(sim_time_get, sim_time_expected)

    def test_get_sim_num_actions(self):
        # arrange
        simulation = self.simulation

        # act
        sim_num_actions_get = simulation.get_sim_num_actions()
        sim_num_actions_expected = simulation.sim_num_actions

        # assert
        self.assertEqual(sim_num_actions_get, sim_num_actions_expected)

    def test_get_events_to_simulate(self):
        # arrange
        simulation = self.simulation

        # act
        events_to_simulate_get = simulation.get_events_to_simulate()
        events_to_simulate_expected = simulation.events_to_simulate

        # assert
        self.assertListEqual(events_to_simulate_get, events_to_simulate_expected)

    def test_run_simulation_abstractmethod(self):
        # arrange
        simulation = self.simulation

        # act

        # assert
        self.assertRaises(NotImplementedError, simulation.run_simulation)
