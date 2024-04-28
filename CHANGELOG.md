# CHANGELOG

## v0.0.2

### New Features and Improvements
- Random drawer generation added to the drawer class. It's now possible to generate only one drawer.
- Improved `get_minimum_offset` method to calculate the minimum offset between columns in the warehouse.
- Created a new module called `Algorithm` where it's possible to insert a new algorithm.
- New methods added to the `Column` and `Carousel` classes: `is_full` and `is_empty`.
- Moved the `gen_materials_and_drawers` static method from `Warehouse` to the `Column` class (for logical reasons).
- Added a `min_height` parameter when randomly generating a material in the `Material` class.

### Bug Fixes and Enhancements
- Fixed random drawers generation in `Drawer` class. There were some problems (raise `ValueError`) when the
  `materials_to_insert` parameter was larger than the `how_many` parameter.
- Fixed `get_num_entries_free` in Column class. There were some problems because the last position of the warehouse was 
  considered multiple times (instead of only once).
- Improved readability `calculate_max_height` method of the drawer class.
- Improved readability `__eq__` method for material class.
- Improved readability and naming of the methods used to decide where to insert a drawer.
- Improved readability and speed of the `_high_position_algorithm`.
- Improved readability of the `gen_rand` method in the `Warehouse` class.
- Added new `__eq__` methods.

### Other
- Refactoring comments, change comment style.
- Added tests.

------------------------------------------------------------------------------------------------------------------------

## [v0.0.1-bachelors-degree-thesis](https://github.com/AndreVale69/simulator-automatic-warehouse/releases/tag/v0.0.1-bachelors-degree-thesis)
- This is an alpha version of the project. It is only made to see how the project was at the start. It corresponds to my bachelor thesis in computer science at the University of Verona. 
  This version should be stable, but it doesn't have any tests (next improvement)! So for now it is not very reliable.