from pandas import Timestamp
from datetime import timedelta
from datetime import datetime
from math import ceil


class Timeline:
    def __init__(self, minimum_time: Timestamp | datetime, maximum_time: Timestamp | datetime):
        self._minimum_time: Timestamp | datetime = minimum_time
        self._maximum_time: Timestamp | datetime = maximum_time
        # default range value (left to right) 1-minute
        self._step: int = 1
        # left time of timeline
        self._actual_left: datetime = minimum_time
        # right time of timeline
        self._actual_right: datetime = self._actual_left + timedelta(minutes=self._step)
        # set num. total tabs
        self._tot_tabs = self.calculate_tot_tabs()
        # default actual tab
        self._actual_tab: int = 1

    def get_minimum_time(self) -> Timestamp | datetime:
        return self._minimum_time

    def get_maximum_time(self) -> Timestamp | datetime:
        return self._maximum_time

    def get_actual_left(self) -> datetime:
        return self._actual_left

    def get_actual_right(self) -> datetime:
        return self._actual_right

    def get_step(self) -> int:
        return self._step

    def calculate_tot_tabs(self) -> int:
        time_left = self.get_minimum_time().time()
        time_right = self.get_maximum_time().time()
        # eventually, calculate days btw min and max
        diff_days = self.get_maximum_time().date() - self.get_minimum_time().date()
        # calculate hours btw min and max
        diff_hours = (timedelta(hours=time_right.hour, minutes=time_right.minute, seconds=time_right.second,
                                microseconds=time_right.microsecond) -
                      timedelta(hours=time_left.hour, minutes=time_left.minute, seconds=time_left.second,
                                microseconds=time_left.microsecond))
        # calculate the total time between these two limits
        total_time: timedelta = diff_hours + diff_days
        # rounding up
        return ceil(total_time.seconds / 60)

    def right_btn_triggered(self):
        # check limit
        if self._actual_tab < self._tot_tabs:
            self._actual_left = self._actual_right
            self._actual_right += timedelta(minutes=self._step)
            self._actual_tab += 1

    def left_btn_triggered(self):
        # check limit
        if self._actual_tab > 1:
            self._actual_right = self._actual_left
            self._actual_left -= timedelta(minutes=self._step)
            self._actual_tab -= 1

    def summary_btn_triggered(self):
        self._actual_left = self.get_minimum_time()
        self._actual_right = self.get_maximum_time()

    def set_step(self, minutes: int):
        # TODO: review this, it's a bit dangerous...
        self._step = minutes

    def actual_tabs(self) -> str:
        # well-format string
        return f'{self._actual_tab}/{self._tot_tabs}'
