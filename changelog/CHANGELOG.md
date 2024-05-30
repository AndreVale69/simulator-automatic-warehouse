# CHANGELOG

## v1.0.0

### New Features and Improvements
- Random tray generation added to the `Tray` class. It's now possible to generate only one tray.
- Improved `get_minimum_offset` method to calculate the minimum offset between columns in the warehouse.
- Improved `gen_rand` method in the `Warehouse` class. Now it cleanup the warehouse and then generate a bay 
  (bool parameter), a buffer (bool parameter), and populates the columns.
- Improved simulation execution. Moved **all** simulation methods from `Warehouse` class to `Simulation` class. 
  The list of moved methods is:
  - `run_simulation`
  - `new_simulation`
  - `go_to_bay`
  - `go_to_buffer`
  - `load_in_carousel`
  - `loading_buffer_and_remove`
  - `vertical_move`
  - `allocate_best_pos`
  - `reach_tray_height`
  - `unload`
  - `load`
  - `horiz_move`
- Improved the logic of the `Simulation` class.
  Created `Simulation` class as superclass and `WarehouseSimulation` as child to have any custom simulation method.
- Improved logic of the `simulation_actions` methods. It now takes two parameters: `tray` and `destination`.
- Created a new module called `Algorithm` where it's possible to insert a new algorithm.
- New methods added to the `Column` and `Carousel` classes: `is_full` and `is_empty`.
- Moved the `gen_materials_and_trays` static method from `Warehouse` to the `Column` class (for logical reasons).
- Moved the `remove_tray` method from `TrayContainer` to the `Column` class.
- Added a `min_height` parameter when randomly generating a material in the `Material` class.
- Added a `cleanup` method to cleanup the warehouse.
- Added a `get_num_columns` method to get the number of columns in the warehouse.
- Added `get_bay_tray` and `get_buffer_tray` methods to the `Carousel` class (useful methods).
- Added `last_position_is_occupied` method to the `Column` class.
- Added `cleanup_columns` and `cleanup_carousel` methods to the `Warehouse` class.
- Added a new exception in `horiz_move` if the offset is not found.
- Added a new exception in `load` if the offset is not found.
- Added default config path if none is specified (`configuration/sample_config.yaml`).
- Added total simulation time.
- Changed the first trayEntry reference. Now the first trayEntry will be the lower limit.
  For example, a tray with three entries; in the container the first trayEntry will be position 2, 
  and entries 0 and 1 are simple trayEntries.
- Changed `Carousel` class signature.
  It doesn't accept a dictionary anymore as parameter, but it wants a `CarouselInfo` class instantiation.
  This was done for clarity.
- Changed `Column` class signature.
  It doesn't accept a dictionary anymore as parameter, but it wants a `ColumnInfo` class instantiation.
  This was done for clarity.
- Changed `get_height_container` method to `get_num_entries`. 
  The first returns the height of the container (config value) 
  and the second returns the number of entries in the warehouse.
- `Drawer` name changed to `Tray`.
- `Deposit` name changed to `Bay`.

### Bug Fixes and Enhancements
- Fixed random trays generation in `Tray` class. There were some problems (raise `ValueError`) when the
  `materials_to_insert` parameter was larger than the `how_many` parameter.
- Fixed `get_num_entries_free` in `Column` class. 
  There were some problems because the last position of the warehouse was considered multiple times 
  (instead of only once).
- Fixed `__hash__` in `Tray` class. It throws an exception because Python can't hash a list.
- Fixed `remove_tray` in the `Carousel` class. 
  It returns true if a tray isn't in the carousel. 
  This fix improves performance because it only checks two items (not the whole container...).
- Fixed `is_empty` in `Column` class. It used a wrong height.
- Fixed `__hash__` in Entry class. It always returns the same value.
- Fixed _file not found_ error if the name of the project's directory was different from `simulator-automatic-warehouse`.
- Improved readability `calculate_max_height` method of the `Tray` class.
- Improved readability `__eq__` method for `Material` class.
- Improved readability and naming of the methods used to decide where to insert a tray.
- Improved readability and speed of the `_high_position_algorithm`.
- Improved readability of the `gen_rand` method in the `Warehouse` class.
- Improved readability between simulation class methods.
- Improved logic for abstract methods. They now throw a `NotImplementedError`.
- Added different prime number in hash method for each class.
- Added new `__eq__` methods.
- Added new `__hash__` methods.
- Changed name of `get_max_num_space` method (`Tray` class) to `get_num_space_occupied`.
- Changed name of `get_height_col` method (`TrayContainer` class) to `get_height_container`.

### Other
- Refactoring comments, change comment style.
- Added tests.

------------------------------------------------------------------------------------------------------------------------

## [v0.0.1-bachelors-degree-thesis](https://github.com/AndreVale69/simulator-automatic-warehouse/releases/tag/v0.0.1-bachelors-degree-thesis)
- This is an alpha version of the project. It is only made to see how the project was at the start. It corresponds to my bachelor thesis in computer science at the University of Verona. 
  This version should be stable, but it doesn't have any tests (next improvement)! So for now it is not very reliable.