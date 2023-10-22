from pandas import Timestamp
from datetime import timedelta
from datetime import datetime


class Timeline:
    def __init__(self, minimum_time: Timestamp | datetime, maximum_time: Timestamp | datetime):
        self.minimum_time: Timestamp | datetime = minimum_time
        self.maximum_time: Timestamp | datetime = maximum_time
        # default range value (left to right) 1-minute
        self.step = 1
        # left time of timeline
        self.actual_left: datetime = minimum_time
        # right time of timeline
        self.actual_right: datetime = self.actual_left + timedelta(minutes=self.step)

    def get_minimum_time(self) -> Timestamp | datetime:
        return self.minimum_time

    def get_maximum_time(self) -> Timestamp | datetime:
        return self.maximum_time

    def get_actual_left(self) -> datetime:
        return self.actual_left

    def get_actual_right(self) -> datetime:
        return self.actual_right

    def get_step(self) -> int:
        return self.step

    def right_btn_triggered(self):
        self.actual_left = self.actual_right
        self.actual_right += timedelta(minutes=self.get_step())

    def left_btn_triggered(self):
        self.actual_right = self.actual_left
        self.actual_left -= timedelta(minutes=self.get_step())

    def summary_btn_triggered(self):
        self.actual_left = self.get_minimum_time()
        self.actual_right = self.get_maximum_time()

    def set_step(self, value: int):
        self.step = value

    def actual_tabs(self) -> str:
        # TODO: to fix
        time_min = self.get_actual_left().time()
        time_max = self.get_actual_right().time()
        # calculate days btw min and max
        diff_days = self.get_actual_right().date() - self.get_actual_left().date()
        # calculate hours btw min and max
        diff_hours = (timedelta(hours=time_max.hour, minutes=time_max.minute, seconds=time_max.second,
                                microseconds=time_max.microsecond) -
                      timedelta(hours=time_min.hour, minutes=time_min.minute, seconds=time_min.second,
                                microseconds=time_min.microsecond))
        # calculate the total time of the simulation
        total_time:timedelta = diff_hours + diff_days
        # calculate the total number of tabs depending on the step value
        num_tabs: int = (total_time.seconds // 60) // self.get_step()
        # well-format string
        return f'1/{num_tabs}'
