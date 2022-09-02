import numpy as np
import debug_library as debug
import useful_functions as us_fun
import warehouse_operations as ware_op
import bash_graphic_construction as bash_grap

# Contains the measurements of the size of the drawers
type = np.dtype([("name", "U30"), ("height", "uint32")])
data_left_column = np.array([], dtype=type)
data_right_column = np.array([], dtype=type)

# Insert all information of automatic warehouse
print("Enter all information of automatic warehouse below\n\n")

# Create a automatic warehouse with default height, otherwise creare with custom height
# TODO the height of left column and the height of right column must be the same!
if int(input("Debug mode? [Yes = 1 / No = 0]: ")) == 1:
    data_left_column = debug.create_left_column(data_left_column)
    data_right_column = debug.create_right_column(data_right_column)
    for i in range(data_right_column.size):
        if data_right_column[i][0] == "Storage":
            storage_area = data_right_column[i][1]
        else:
            if data_right_column[i][0] == "Buffer":
                buffer_area = data_right_column[i][1]
            else:
                if data_right_column[i][0] == "Hole":
                    hole = data_right_column[i][1]
else:
    print("Create left column...\n")
    data_left_column = ware_op.column_construction(data_left_column)

    print("\n\nCreate right column...")
    data_right_column = ware_op.column_construction(data_right_column)

    storage_area = int(input("Insert height storage area: "))
    data_right_column = np.insert(data_right_column, data_right_column.size, ("Storage", storage_area))

    buffer_area = int(input("Insert height buffer area: "))
    data_right_column = np.insert(data_right_column, data_right_column.size, ("Buffer", buffer_area))

    hole = int(input("Insert height right hole: "))
    data_right_column = np.insert(data_right_column, data_right_column.size, ("Hole", hole))

# Check arrays
print(data_left_column)
print(data_right_column)

# Some information...
numbers_drawer_left = ware_op.count_drawers(data_left_column)
numbers_drawer_right = ware_op.count_drawers(data_right_column)
numbers_space_left = ware_op.count_space(data_left_column)
numbers_space_right = ware_op.count_space(data_right_column)

print("\nNumbers drawers left : " + str(numbers_drawer_left))
print("Numbers drawers right: " + str(numbers_drawer_right))
print("Numbers space left   : " + str(numbers_space_left))
print("Numbers space right  : " + str(numbers_space_right))

height_left_column = ware_op.height_left_column(data_left_column)
height_right_column = ware_op.height_right_column(data_right_column, storage_area, buffer_area, hole)
height_warehouse = height_left_column if height_left_column > height_right_column else height_right_column

print("Height left column        : " + str(height_left_column))
print("Height right column       : " + str(height_right_column))
print("Height automatic warehouse: " + str(height_warehouse))

# Print warehouse; TODO to finish :(
bash_grap.print_warehouse(data_right_column)

# OLD function
#bash_grap.print_warehouse(height_left,
#                          height_right_upper,
#                          height_drawer_extreme,
#                          height_drawer_left,
#                          height_drawer_right_upper,
#                          numbers_drawer_left,
#                          numbers_drawer_right)
