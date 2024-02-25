from pandas import DataFrame, Series, Timedelta, Timestamp, Period
from enum import Enum
from sim.status_warehouse.simulate_events.action_enum import ActionEnum


class TimeEnum(Enum):
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


    def _get_start(self) -> Series:
        return self._warehouse_actions["Start"]


    def _get_finish(self) -> Series:
        return self._warehouse_actions["Finish"]


    def _get_type_of_action(self):
        return self._warehouse_actions["Type of Action"]


    def actions_started_every(self, time: TimeEnum) -> DataFrame:
        """
        Calculate a Series with a number of rows with datetime and their relative count (number of actions started ONLY).
        The counter refers to all actions in the simulation.

        @param time: Time requested.
        @return: A table of actions started each "time" given as a parameter.
                 The DataFrame contains two columns: Start and Count.
        """
        value_counts: Series = self._get_start().dt.to_period(time.value).value_counts(sort=False)
        start = value_counts.index.to_list()
        counts = value_counts.to_list()
        return DataFrame([{'Start': str(start[index]), 'Count': counts[index]} for index in range(value_counts.size)])


    def actions_finished_every(self, time: TimeEnum) -> DataFrame:
        """
        Calculate a Series with a number of rows with datetime and their relative count (number of actions finished ONLY).
        The counter refers to all actions in the simulation.

        @param time: Time requested.
        @return: A table of actions finished each "time" given as a parameter.
                 The DataFrame contains two columns: Finish and Count.
        """
        value_counts: Series = self._get_finish().dt.to_period(time.value).value_counts(sort=False)
        finish = value_counts.index.to_list()
        counts = value_counts.to_list()
        return DataFrame([{
            'Finish': str(finish[index]),
            'Count': counts[index]
        } for index in range(value_counts.size)])


    def actions_completed_every(self, time: TimeEnum) -> DataFrame:
        """
        Calculate a Series with Start datetime, Finish datetime and their relative count.
        If an order is started at (e.g.) 10:58 and finished at 11:05, it will not be counted in the 10-hour counter.
        So it's possible to find some lines with a Start time different from the Finish time.

        @param time: Time requested.
        @return: A table of actions completed each "time" given as a parameter.
                 The DataFrame contains three columns: Start, Finish, and Count.
        """
        value_counts: Series = DataFrame({
            'Start': self._get_start().dt.to_period(time.value),
            'Finish': self._get_finish().dt.to_period(time.value)
        }).value_counts(sort=False)
        start_finish: list[tuple[Period, Period]] = value_counts.index.to_list()
        counts = value_counts.to_list()
        return DataFrame([{
                'Start': str(start_finish[index][0]),
                'Finish': str(start_finish[index][1]),
                'Count': counts[index]
        } for index in range(value_counts.size)])


    def action_started_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame:
        """
        Calculate a Series with a number of rows with datetime and their relative count (number of actions started ONLY).
        The counter only refers to the action specified in the "action" parameter.

        @param action: action requested.
        @param time: time requested.
        @return: a table of the requested action started each "time" given as a parameter.
                 The DataFrame contains three columns: Type of Action, Start, and Count.
        """
        action_val: str = action.value
        value_counts: Series = DataFrame({
            'type_of_action': self._get_type_of_action(),
            'Start': self._get_start().dt.to_period(time.value)
        }).value_counts(sort=False).get(action_val)
        start: list[Period] = value_counts.index.to_list()
        counts: list[int] = value_counts.to_list()
        return DataFrame([{
            'Type of Action': action_val,
            'Start': str(start[index]),
            'Count': counts[index]
        } for index in range(value_counts.size)])


    def action_finished_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame:
        """
        Calculate a Series with a number of rows with datetime and their relative count (number of actions finished ONLY).
        The counter only refers to the action specified in the "action" parameter.

        @param action: action requested.
        @param time: time requested.
        @return: a table of the requested action finished each "time" given as a parameter.
                 The DataFrame contains three columns: Type of Action, Finish, and Count.
        """
        action_val: str = action.value
        value_counts: Series = DataFrame({
            'type_of_action': self._get_type_of_action(),
            'Finish': self._get_finish().dt.to_period(time.value)
        }).value_counts(sort=False).get(action.value)
        finish: list[Period] = value_counts.index.to_list()
        counts: list[int] = value_counts.to_list()
        return DataFrame([{
            'Type of Action': action_val,
            'Finish': str(finish[index]),
            'Count': counts[index]
        } for index in range(value_counts.size)])


    def action_completed_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame:
        """
        Request the action to be completed, specifying the action requested and the time period.
        Calculate a Series with Start datetime, Finish datetime and their relative count.
        If an order is started at (e.g.) 10:58 and finished at 11:05, it will not be counted in the 10-hour counter.
        So it's possible to find some lines with a Start time different from the Finish time.

        @param action: the type of action to consider.
        @param time: time period requested.
        @return: a table of "action" actions completed each "time", both given as parameters.
                 The DataFrame contains three columns: Type of Action, Start, Finish, and Count
        """
        action_val: str = action.value
        value_counts: Series = DataFrame({
            'type_of_action': self._get_type_of_action(),
            'Start': self._get_start().dt.to_period(time.value),
            'Finish': self._get_finish().dt.to_period(time.value)
        }).value_counts(sort=False).get(action.value)
        start_finish: list[tuple[Period, Period]] = value_counts.index.to_list()
        counts: list[int] = value_counts.to_list()
        return DataFrame([{
            'Type of Action': action_val,
            'Start': str(start_finish[index][0]),
            'Finish': str(start_finish[index][1]),
            'Count': counts[index]
        } for index in range(value_counts.size)])


    def count_action_completed(self, action: ActionEnum) -> int:
        """
        Calculate how many actions are completed for a given action.

        @param action: count calculation actions
        @return: how many actions are completed in the whole simulation.
        """
        return self._warehouse_actions.groupby("Type of Action").count().get("Finish").get(action.value)


    def start_time_simulation(self) -> Timestamp:
        """
        Get the start of the simulation.

        @return: the start of the simulation as pandas Timestamp.
        """
        return self._get_start()[0]


    def finish_time_simulation(self) -> Timestamp:
        """
        Get the finish of the simulation.

        @return: the finish of the simulation as pandas Timestamp.
        """
        return self._get_finish()[self._get_finish().size - 1]


    def total_simulation_time(self) -> Timedelta:
        """
        Get the total time of the simulation.

        @return: the total time of the simulation as pandas Timedelta.
        """
        return self.finish_time_simulation() - self.start_time_simulation()
