## TODO: high priority

### Validator

- [x] The height property of each column can't be greater than the height of the warehouse (height_warehouse).
- [x] The default_height_space should be a multiple of any column, otherwise the number of drawers in a column could be float (impossible).
- [ ] If a column has the same x_offset as the carousel, then that column is above the carousel. 
   This means that:
   1. The sum of the height of the column plus the height of the hole, 
      buffer and bay of the carousel should be equal to or less than height_warehouse.
   2. The length should be equal.
- [ ] Take an x_offset, make width / 2, create a left and right border and check that the border is not equal to another. 
   If they are the same, the distance between the two columns is zero.
- [x] height_last_position should be a multiple of default_height_space 
   because it indicates how many entries are in the last position of the column.
- [ ] Two columns can't have the same x_offset.
- [ ] The length/width/height of the trays placed in the storage can't be greater than the length/width/height of 
   the column in which it is placed.
- [ ] The number of trays to be generated cannot be greater than the sum of the heights of the columns 
   (not including the carousel).

------------------------------------------------------------------------------------------------------------------------

## TODO Features

1. Each tray cannot have unlimited materials.
   We have to calculate the height, length and width of each material and check if there is more space 
   (and if it doesn't exceed the limit of the lift).
