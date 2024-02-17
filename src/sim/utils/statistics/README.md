# Warehouse Statistics API documentation

This file contains a list of the API available within the `WarehouseStatistics` class.
The main purpose of this object is to provide a set of methods to allow the programmer to easily manipulate the data of the 
simulation.

`WarehouseStatistics` has a large use of `functools.lru_cache` because its internal variables don't change over time. In fact, only the input parameter can change, but the output will always be the same.

## API List

The following is a list of the methods. Each one is decorated with a description and an example of the object returned.

### WarehouseStatistics `__init__`

To instantiate the class, all that is required are the items obtained from a Pandas `DataFrame`. 
This object must be instantiated using the history of the warehouse simulation:
```python
from pandas import DataFrame
from sim.utils.statistics.warehouse_statistics import WarehouseStatistics
from src.sim.warehouse import Warehouse

warehouse = Warehouse()
warehouse.run_simulation()
warehouse_statistics = WarehouseStatistics(
    DataFrame(warehouse.get_simulation().get_store_history().items)
)
```

------------------------------------------------------------------------------------------------------------------------

### `actions_started_every(self, time: TimeEnum) -> Series`

### `actions_finished_every(self, time: TimeEnum) -> Series`

### `actions_completed_every(self, time: TimeEnum) -> Series`

------------------------------------------------------------------------------------------------------------------------

### `action_started_every(self, action: ActionEnum, time: TimeEnum) -> Series`

### `action_finished_every(self, action: ActionEnum, time: TimeEnum) -> Series`

### `action_completed_every(self, action: ActionEnum, time: TimeEnum) -> Series`

------------------------------------------------------------------------------------------------------------------------

### `count_action_completed(self, action: ActionEnum) -> int`

------------------------------------------------------------------------------------------------------------------------

### `start_time_simulation(self) -> Timestamp`

### `finish_time_simulation(self) -> Timestamp`

### `total_simulation_time(self) -> Timestamp`