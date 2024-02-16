from pandas import DataFrame, Series
from functools import lru_cache


class WarehouseStatistics:
    def __init__(self, warehouse_actions: DataFrame):
        self._warehouse_actions = warehouse_actions

    @lru_cache
    def orders_started_every_hour(self) -> Series:
        """
        Calculate a Series with a number of rows with datetime and their relative count (number of orders started ONLY).

        @return: a table of orders started every hour.
        """
        # count how many orders have started each hour (does not sort, so it keeps the real time order)
        return self._warehouse_actions["Start"].dt.to_period("H").value_counts(sort=False)

    @lru_cache
    def orders_finished_every_hour(self) -> Series:
        """
        Calculate a Series with a number of rows with datetime and their relative count (number of orders finished ONLY).

        @return: a table of orders finished every hour.
        """
        # count how many orders has finished each hour
        return self._warehouse_actions["Finish"].dt.to_period("H").value_counts(sort=False)

    @lru_cache
    def orders_completed_every_hour(self) -> Series:
        """
        Calculate a Series with Start datetime, Finish datetime and their relative count.
        In this case, it's possible to find rows without a Start datetime.
        The reason is simple: if an order is started at (e.g.) 10:58 and finished at 11:05,
                              it will not be counted in the 10-hour counter.

        @return: a table of orders completed every hour.
        """
        # create a unique matrix and count how many values are the same at each hour
        return DataFrame({
            'Start': self._warehouse_actions["Start"].dt.to_period("H"),
            'Finish': self._warehouse_actions["Finish"].dt.to_period("H")
        }).value_counts(sort=False)
