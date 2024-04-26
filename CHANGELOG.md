# CHANGELOG

## v0.0.2

### New Features and Improvements
- Random drawer generation added to the drawer class. It's now possible to generate only one drawer.

### Bug Fixes and Enhancements
- Fixed random drawers generation in drawer class. 

  There were some problems (raise `ValueError`) when the `materials_to_insert` parameter was larger than the `how_many` 
  parameter. 
- Improved readability `calculate_max_height` method of the drawer class.
- Improved readability `__eq__` method for material class.
- Added new `__eq__` methods.

### Other
- Refactoring comments, change comment style.
- Added tests.

------------------------------------------------------------------------------------------------------------------------

## [v0.0.1-bachelors-degree-thesis](https://github.com/AndreVale69/simulator-automatic-warehouse/releases/tag/v0.0.1-bachelors-degree-thesis)
- This is an alpha version of the project. It is only made to see how the project was at the start. It corresponds to my bachelor thesis in computer science at the University of Verona. 
  This version should be stable, but it doesn't have any tests (next improvement)! So for now it is not very reliable.