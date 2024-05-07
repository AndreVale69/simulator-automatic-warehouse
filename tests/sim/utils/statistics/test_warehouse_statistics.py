import unittest

from numpy import int64
from pandas import DataFrame, Timestamp, Timedelta

from src.sim.status_warehouse.simulate_events.action_enum import ActionEnum
from src.sim.utils.statistics.warehouse_statistics import WarehouseStatistics, TimeEnum
from src.sim.warehouse import Warehouse


class TestWarehouseStatistics(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.run_simulation()
        self.warehouse_statistics = WarehouseStatistics(DataFrame(self.warehouse.get_simulation().get_store_history().items))

    def test_actions_started_every(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        res = warehouse_statistics.actions_started_every(TimeEnum.MINUTE)

        # assert
        self.assertIsInstance(res, DataFrame)
        self.assertIsNotNone(res.get('Start'))
        self.assertIsNotNone(res.get('Count'))

    def test_actions_finished_every(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        res = warehouse_statistics.actions_finished_every(TimeEnum.MINUTE)

        # assert
        self.assertIsInstance(res, DataFrame)
        self.assertIsNotNone(res.get('Finish'))
        self.assertIsNotNone(res.get('Count'))

    def test_actions_completed_every(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        res = warehouse_statistics.actions_completed_every(TimeEnum.MINUTE)

        # assert
        self.assertIsInstance(res, DataFrame)
        self.assertIsNotNone(res.get('Start'))
        self.assertIsNotNone(res.get('Finish'))
        self.assertIsNotNone(res.get('Count'))

    def test_action_started_every(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        res = warehouse_statistics.action_started_every(ActionEnum.EXTRACT_DRAWER, TimeEnum.MINUTE)

        # assert
        self.assertIsInstance(res, DataFrame)
        self.assertIsNotNone(res.get('Type of Action'))
        self.assertIsNotNone(res.get('Start'))
        self.assertIsNotNone(res.get('Count'))
        self.assertNotIn(False, [action == ActionEnum.EXTRACT_DRAWER.value for action in res.get('Type of Action')])

    def test_action_finished_every(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        res = warehouse_statistics.action_finished_every(ActionEnum.EXTRACT_DRAWER, TimeEnum.MINUTE)

        # assert
        self.assertIsInstance(res, DataFrame)
        self.assertIsNotNone(res.get('Type of Action'))
        self.assertIsNotNone(res.get('Finish'))
        self.assertIsNotNone(res.get('Count'))
        self.assertNotIn(False, [action == ActionEnum.EXTRACT_DRAWER.value for action in res.get('Type of Action')])

    def test_action_completed_every(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        res = warehouse_statistics.action_completed_every(ActionEnum.EXTRACT_DRAWER, TimeEnum.MINUTE)

        # assert
        self.assertIsInstance(res, DataFrame)
        self.assertIsNotNone(res.get('Type of Action'))
        self.assertIsNotNone(res.get('Start'))
        self.assertIsNotNone(res.get('Finish'))
        self.assertIsNotNone(res.get('Count'))
        self.assertNotIn(False, [action == ActionEnum.EXTRACT_DRAWER.value for action in res.get('Type of Action')])

    def test_count_action_completed(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        expected = warehouse_statistics._warehouse_actions.groupby("Type of Action").count().get("Finish").get(ActionEnum.EXTRACT_DRAWER.value)
        res = warehouse_statistics.count_action_completed(ActionEnum.EXTRACT_DRAWER)

        # assert
        self.assertIsInstance(res, int64)
        self.assertEqual(res, expected)

    def test_start_time_simulation(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        expected = warehouse_statistics._warehouse_actions["Start"][0]
        res = warehouse_statistics.start_time_simulation()

        # assert
        self.assertIsInstance(res, Timestamp)
        self.assertEqual(res, expected)

    def test_finish_time_simulation(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        expected = warehouse_statistics._warehouse_actions["Finish"][warehouse_statistics._warehouse_actions["Finish"].size-1]
        res = warehouse_statistics.finish_time_simulation()

        # assert
        self.assertIsInstance(res, Timestamp)
        self.assertEqual(res, expected)

    def test_total_simulation_time(self):
        # arrange
        warehouse_statistics = self.warehouse_statistics

        # act
        expected = warehouse_statistics.finish_time_simulation() - warehouse_statistics.start_time_simulation()
        res = warehouse_statistics.total_simulation_time()

        # assert
        self.assertIsInstance(res, Timedelta)
        self.assertEqual(res, expected)