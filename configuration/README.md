## TODO

1. The height property of each column can't be greater than the height of the warehouse (height_warehouse).
2. The default_height_space should be a multiple of any column, otherwise the number of drawers in a column could be float (impossible).
3. If a column has the same x_offset as the carousel, then that column is above the carousel. 
   This means that:
   1. The sum of the height of the column plus the height of the hole, 
      buffer and bay of the carousel should be equal to or less than height_warehouse.
   2. The length should be equal.
4. Take an x_offset, make width / 2, create a left and right border and check that the border is not equal to another. 
   If they are the same, the distance between the two columns is zero.
5. height_last_position should be a multiple of default_height_space 
   because it indicates how many entries are in the last position of the column.
6. Two columns can't have the same x_offset.