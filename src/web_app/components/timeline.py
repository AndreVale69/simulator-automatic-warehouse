from datetime import datetime
from datetime import timedelta, time
from math import ceil

import plotly.express as px
import plotly.graph_objs as go
from pandas import Timestamp, DataFrame


def _create_timedelta(times: time) -> timedelta:
    return timedelta(
        hours=times.hour,
        minutes=times.minute,
        seconds=times.second,
        microseconds=times.microsecond
    )


class Timeline:
    def __init__(self, datas: list[dict], step: int = 1):
        # create dataframe used to Timeline
        self._df = DataFrame(datas)
        # saves these variables to avoid high calculates computing
        self._total_time: timedelta | None = None
        self._diff_hours: timedelta | None = None
        self._diff_days: timedelta | None = None
        self._maximum_time: time | None = None
        self._minimum_time: time | None = None

        # Take the minimum and maximum time of the simulation
        self._minimum: Timestamp | datetime = self._df.min().get('Start')
        self._maximum: Timestamp | datetime = self._df.max().get('Finish')
        # default range value (left to right) 1-minute
        self._step: int = step
        # left time of timeline
        self._actual_left: datetime = self._minimum
        # right time of timeline
        self._actual_right: datetime = self._actual_left + timedelta(minutes=self._step)
        # set num. total tabs
        self._tot_tabs: int = self.calculate_tot_tabs()
        # default actual tab
        self._actual_tab: int = 1
        self._create_timeline_fig()

    def _create_timeline_fig(self):
        # See https://plotly.com/python/px-arguments/ for more options
        # Create the timeline
        self._figure = px.timeline(self._df,
                          x_start="Start", x_end="Finish", y="Type of Action",
                          range_x=[self._actual_left, self._actual_right],
                          color="Type of Action")
        self._figure.update_yaxes(autorange="reversed")  # otherwise, tasks are listed from the bottom up
        # If you want a linear timeline:
        # fig.layout.xaxis.type = 'linear'
        self._figure.layout.xaxis.type = 'date'
        # create slider
        self._figure.update_xaxes(rangeslider=dict(visible=True, range=[self._minimum, self._maximum]))
        # If you want a rangeselector to zoom on each section
        # See more: https://plotly.com/python/range-slider/

    def get_figure(self) -> go.Figure:
        return self._figure

    def get_dataframe(self) -> DataFrame:
        return self._df

    def get_minimum_time(self) -> Timestamp | datetime:
        return self._minimum

    def get_maximum_time(self) -> Timestamp | datetime:
        return self._maximum

    def get_actual_left(self) -> datetime:
        return self._actual_left

    def get_actual_right(self) -> datetime:
        return self._actual_right

    def get_step(self) -> int:
        return self._step

    def get_actual_tab(self) -> int:
        return self._actual_tab

    def get_tot_tabs(self) -> int:
        return self._tot_tabs

    def get_tot_time_sim(self) -> int:
        # minutes
        return ceil(self._total_time.total_seconds() / 60)

    def calculate_tot_tabs(self) -> int:
        self._minimum_time = self._minimum.time()
        self._maximum_time = self._maximum.time()
        # eventually, calculate days btw min and max
        self._diff_days = self._maximum.date() - self._minimum.date()
        # calculate hours btw min and max
        self._diff_hours = _create_timedelta(self._maximum_time) - _create_timedelta(self._minimum_time)
        # calculate the total time between these two limits
        self._total_time: timedelta = self._diff_hours + self._diff_days
        # rounding up
        return ceil((self._total_time.seconds / 60) / self._step)

    def right_btn_triggered(self):
        # increase iff it isn't the limit
        if self._actual_tab < self._tot_tabs:
            self._actual_tab += 1

    def right_end_btn_triggered(self):
        self._actual_tab = self._tot_tabs

    def left_btn_triggered(self):
        # decrease iff it isn't the limit
        if self._actual_tab > 1:
            self._actual_tab -= 1

    def left_end_btn_triggered(self):
        self._actual_tab = 1

    def summary_btn_triggered(self):
        self._actual_left = self._minimum
        self._actual_right = self._maximum

    def set_step(self, minutes: int):
        self._step = minutes
        self._tot_tabs = self.calculate_tot_tabs()
        # check limit
        self.set_actual_view(self._tot_tabs if self._actual_tab > self._tot_tabs else self._actual_tab)

    def set_actual_view(self, val_actual_tab: int):
        # updates actual tab
        self._actual_tab = val_actual_tab
        # updates limits
        self._actual_right = self._minimum + timedelta(minutes=(self._step * self._actual_tab))
        self._actual_left = self._minimum + timedelta(minutes=(self._step * (self._actual_tab - 1)))
