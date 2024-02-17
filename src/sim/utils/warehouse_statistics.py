from pandas import DataFrame, Series, Timedelta, Timestamp
from functools import lru_cache
from enum import Enum
from sim.status_warehouse.Simulate_Events.action_enum import ActionEnum


class TimeType(Enum):
    NANOSECONDS = 'ns'
    MICROSECONDS = 'us'
    MILLISECONDS = 'ms'
    SECOND = 's'
    MINUTE = 'min'
    HOUR = 'h'
    DAY = 'D'
    BUSINESS_DAY = 'B'
    MONTH = 'M'
    YEAR = 'Y'


class WarehouseStatistics:
    def __init__(self, warehouse_actions: DataFrame):
        self._warehouse_actions = warehouse_actions

    @lru_cache
    def _get_start(self) -> Series:
        return self._warehouse_actions["Start"]

    @lru_cache
    def _get_finish(self) -> Series:
        return self._warehouse_actions["Finish"]

    @lru_cache
    def actions_started_every(self, time: TimeType) -> Series:
        """
        Calculate a Series with a number of rows with datetime and their relative count (number of orders started ONLY).

        @param time: time requested.
        @return: a table of orders started each "time" given as a parameter.
        """
        return self._get_start().dt.to_period(time.value).value_counts(sort=False)

    @lru_cache
    def actions_finished_every(self, time: TimeType) -> Series:
        """
        Calculate a Series with a number of rows with datetime and their relative count (number of orders finished ONLY).

        @param time: time requested.
        @return: a table of orders finished each "time" given as a parameter.
        """
        return self._get_finish().dt.to_period(time.value).value_counts(sort=False)

    @lru_cache
    def actions_completed_every(self, time: TimeType) -> Series:
        """
        Calculate a Series with Start datetime, Finish datetime and their relative count.
        In this case, it's possible to find rows without a Start datetime.
        The reason is simple: if an order is started at (e.g.) 10:58 and finished at 11:05,
                              it will not be counted in the 10-hour counter.

        @param time: time requested.
        @return: a table of orders completed each "time" given as a parameter.
        """
        return DataFrame({
            'Start': self._get_start().dt.to_period(time.value),
            'Finish': self._get_finish().dt.to_period(time.value)
        }).value_counts(sort=False)

    @lru_cache
    def action_completed_every(self, action: ActionEnum, time: TimeType) -> Series:
        """
        Request the action to be completed, specifying the action requested and the time period.
        Calculate a Series with Start datetime, Finish datetime and their relative count.
        In this case, it's possible to find rows without a Start datetime.
        The reason is simple: if an order is started at (e.g.) 10:58 and finished at 11:05,
                              it will not be counted in the 10-hour counter.

        @param action: the type of action to consider.
        @param time: time period requested.
        @return: a table of "action" actions completed each "time", both given as parameters.
        """
        return DataFrame({
            'type_of_action': self._warehouse_actions["Type of Action"],
            'Start': self._get_start().dt.to_period(time.value),
            'Finish': self._get_finish().dt.to_period(time.value)
        }).value_counts(sort=False).get(action.value)

    @lru_cache
    def counts_action_completed(self, action: ActionEnum) -> int:
        """
        Calculate how many actions are completed for a given action.

        @param action: count calculation actions
        @return: how many actions are completed in the whole simulation.
        """
        return self._warehouse_actions.groupby("Type of Action").count().get("Finish").get(action.value)

    @lru_cache
    def start_time_simulation(self) -> Timestamp:
        """
        Get the start of the simulation.

        @return: the start of the simulation as pandas Timestamp.
        """
        return self._get_start()[0]

    @lru_cache
    def finish_time_simulation(self) -> Timestamp:
        """
        Get the finish of the simulation.

        @return: the finish of the simulation as pandas Timestamp.
        """
        return self._get_finish()[self._get_finish().size - 1]

    @lru_cache
    def total_simulation_time(self) -> Timedelta:
        """
        Get the total time of the simulation.

        @return: the total time of the simulation as pandas Timedelta.
        """
        return self.finish_time_simulation() - self.start_time_simulation()
