# Warehouse Statistics API documentation

This file contains a list of the API available within the `WarehouseStatistics` class.
The main purpose of this object is to provide a set of methods to allow the programmer to easily manipulate the data of the
simulation.

## API List

The following is a list of the methods. Each one is decorated with a description and an example of the object returned.

- [Warehouse Statistics API documentation](#warehouse-statistics-api-documentation)
  - [API List](#api-list)
    - [How to instantiate](#how-to-instantiate)
      - [WarehouseStatistics](#warehousestatistics)
    - [Count the total number of actions at a given time](#count-the-total-number-of-actions-at-a-given-time)
      - [`actions_started_every(self, time: TimeEnum) -> DataFrame`](#actions_started_everyself-time-timeenum---dataframe)
      - [`actions_finished_every(self, time: TimeEnum) -> DataFrame`](#actions_finished_everyself-time-timeenum---dataframe)
      - [`actions_completed_every(self, time: TimeEnum) -> DataFrame`](#actions_completed_everyself-time-timeenum---dataframe)
    - [Count the total number of a given action at a given time](#count-the-total-number-of-a-given-action-at-a-given-time)
      - [`action_started_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame`](#action_started_everyself-action-actionenum-time-timeenum---dataframe)
      - [`action_finished_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame`](#action_finished_everyself-action-actionenum-time-timeenum---dataframe)
      - [`action_completed_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame`](#action_completed_everyself-action-actionenum-time-timeenum---dataframe)
    - [Count the total amount of a given action in the whole simulation](#count-the-total-amount-of-a-given-action-in-the-whole-simulation)
      - [`count_action_completed(self, action: ActionEnum) -> int`](#count_action_completedself-action-actionenum---int)
    - [Simulation time](#simulation-time)
      - [`start_time_simulation(self) -> Timestamp`](#start_time_simulationself---timestamp)
      - [`finish_time_simulation(self) -> Timestamp`](#finish_time_simulationself---timestamp)
      - [`total_simulation_time(self) -> Timedelta`](#total_simulation_timeself---timedelta)

------------------------------------------------------------------------------------------------------------------------

### How to instantiate

#### WarehouseStatistics

To instantiate the class, all that is required are the items obtained from a Pandas `DataFrame`. 
This object must be instantiated using the history of the warehouse simulation:

```python
from pandas import DataFrame
from automatic_warehouse.utils.statistics.warehouse_statistics import WarehouseStatistics
from automatic_warehouse.simulation.simulation_type.warehouse_simulation import WarehouseSimulation
from automatic_warehouse.warehouse import Warehouse

warehouse = Warehouse()
simulation = WarehouseSimulation(warehouse)
simulation.run_simulation()
warehouse_statistics = WarehouseStatistics(
    DataFrame(simulation.get_store_history_dataframe())
)
```

------------------------------------------------------------------------------------------------------------------------

### Count the total number of actions at a given time

The following APIs return a Pandas object called DataFrame 
([link to the official documentation](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)).

#### `actions_started_every(self, time: TimeEnum) -> DataFrame`

Given a certain time, the method calculates how many actions have only been started. 
The finish time is not considered. 
As you can see in the example below, the returned DataFrame contains two columns: 
the total number of actions performed and the time at which they were started.

| Start            | Count |
|:-----------------|:------|
| 2024-02-17 12:00 | 201   |
| 2024-02-17 13:00 | 404   |
| 2024-02-17 14:00 | 395   |


#### `actions_finished_every(self, time: TimeEnum) -> DataFrame`

The same logic as [`actions_started_every`](#actions_started_everyself-time-timeenum---dataframe) but with the actions 
that are only finished.

| Finish           | Count |
|:-----------------|:------|
| 2024-02-17 12:00 | 200   |
| 2024-02-17 13:00 | 404   |
| 2024-02-17 14:00 | 396   |


#### `actions_completed_every(self, time: TimeEnum) -> DataFrame`

A merge of the previous two, but this DataFrame counts how many actions are started and finished in the same time, 
given as a parameter.
As you can see in the example, some rows contain the same start time. 
These rows show how many actions are started before the finish time.

For example, if an action starts at (e.g.) 10:58 and ends at 11:05, it will not be counted in the 10-hour counter.

| Start            | Finish           | Count |
|:-----------------|:-----------------|:------|
| 2024-02-17 12:00 | 2024-02-17 12:00 | 200   |
| 2024-02-17 12:00 | 2024-02-17 13:00 | 1     |
| 2024-02-17 13:00 | 2024-02-17 13:00 | 403   |
| 2024-02-17 13:00 | 2024-02-17 14:00 | 1     |
| 2024-02-17 14:00 | 2024-02-17 14:00 | 395   |


------------------------------------------------------------------------------------------------------------------------

### Count the total number of a given action at a given time

These methods have the same logic as the functions in 
[Count the total number of actions at a given time](#count-the-total-number-of-actions-at-a-given-time) 
section, but the following refers to a single action given as a parameter.

#### `action_started_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame`

An example of how to call: `warehouse_statistics.action_started_every(ActionEnum.EXTRACT_TRAY, TimeEnum.HOUR)`

| Start            | count |
|:-----------------|:------|
| 2024-02-17 12:00 | 53    |
| 2024-02-17 13:00 | 93    |
| 2024-02-17 14:00 | 95    |


#### `action_finished_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame`

An example of how to call: `warehouse_statistics.action_finished_every(ActionEnum.EXTRACT_TRAY, TimeEnum.HOUR)`

| Finish           | count |
|:-----------------|:------|
| 2024-02-17 12:00 | 52    |
| 2024-02-17 13:00 | 94    |
| 2024-02-17 14:00 | 95    |


#### `action_completed_every(self, action: ActionEnum, time: TimeEnum) -> DataFrame`

An example of how to call: `warehouse_statistics.action_completed_every(ActionEnum.EXTRACT_TRAY, TimeEnum.HOUR)`

|   | Type of Action | Start            | Finish           | Count |
|:--|:---------------|:-----------------|:-----------------|:------|
| 0 | ExtractTray    | 2024-02-18 14:00 | 2024-02-18 14:00 | 82    |
| 1 | ExtractTray    | 2024-02-18 14:00 | 2024-02-18 15:00 | 1     |
| 2 | ExtractTray    | 2024-02-18 15:00 | 2024-02-18 15:00 | 93    |
| 3 | ExtractTray    | 2024-02-18 15:00 | 2024-02-18 16:00 | 1     |
| 4 | ExtractTray    | 2024-02-18 16:00 | 2024-02-18 16:00 | 73    |



------------------------------------------------------------------------------------------------------------------------

### Count the total amount of a given action in the whole simulation

#### `count_action_completed(self, action: ActionEnum) -> int`

The number of times an action has been completed. 
Note: any action that isn't completed is not counted.

------------------------------------------------------------------------------------------------------------------------

### Simulation time

#### `start_time_simulation(self) -> Timestamp`

Return the start time of the simulation as a Pandas Timestamp 
([link to the official documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html)).

For example: `pandas.Timestamp('2024-02-17 12:29:59.124635')`

#### `finish_time_simulation(self) -> Timestamp`

Return the finish time of the simulation as a Pandas Timestamp.

For example: `pandas.Timestamp('2024-02-17 14:59:48.234510')`

#### `total_simulation_time(self) -> Timedelta`

Return the total time of the simulation as a Pandas Timedelta
([link to the official documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html)).

For example: `pandas.Timedelta('0 days 02:29:49.109875')`
