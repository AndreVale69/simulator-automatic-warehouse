import numpy as np
import manual_warehouse as manual
import warehouse_operations as wo
import bash_graphic_construction as bgc

# Contains the measurements of the size of the drawers
type = np.dtype([("name", "U30"), ("height", "uint32")])
data_left_column = np.array([], dtype=type)
data_right_column = np.array([], dtype=type)

# Insert all information of automatic warehouse
print("\nEnter all information of automatic warehouse below\n")

# Create a automatic warehouse with default height, otherwise creare with custom height
if int(input("Debug mode? [Yes = 1 / No = 0]: ")) == 1:
    data_left_column = manual.create_left_column(data_left_column)
    height_left_column = wo.height_left_column(data_left_column)

    data_right_column = manual.create_right_column(data_right_column)
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
    is_valid = 0
    while is_valid == 0:
        print("Create left column...\n")
        data_left_column = wo.column_construction(data_left_column)

        height_left_column = wo.height_left_column(data_left_column)
        print("\nAttention! The height of left column is: " + str(height_left_column) + "\nThe height of right column must be the same.")

        buffer_area = int(input("Insert height buffer area: "))
        data_right_column = np.insert(data_right_column, 0, ("Buffer", buffer_area))

        storage_area = int(input("Insert height storage area: "))
        data_right_column = np.insert(data_right_column, 1, ("Storage", storage_area))

        hole = int(input("Insert height right hole: "))
        data_right_column = np.insert(data_right_column, 2, ("Hole", hole))

        tmp_height_right = wo.height_right_column(data_right_column)
        
        if tmp_height_right > height_left_column:
            print("\n!ERROR!\nThe height of right column (" + str(tmp_height_right) + ") is greater than the height of left column (" + str(height_left_column) + ")\n")
            break
        else:
            if tmp_height_right == height_left_column:
                print("\n!ERROR!\nThe height of left column (" + str(height_left_column) + ") is the same of the height of right column (" + str(tmp_height_right) + ")\n")
                break
        
        print("\nCurrent right height: " + str(tmp_height_right) + "\nLeft height: " + str(height_left_column))

        print("\nCreate right column...")
        data_right_column = wo.column_construction(data_right_column, data_left_column, True)

        is_valid = 1

# Check arrays
print(data_left_column)
print(data_right_column)

# Some information...
numbers_drawer_left = wo.count_drawers(data_left_column)
numbers_drawer_right = wo.count_drawers(data_right_column)
numbers_space_left = wo.count_space(data_left_column)
numbers_space_right = wo.count_space(data_right_column)

print("\nNumbers drawers left : " + str(numbers_drawer_left))
print("Numbers drawers right: " + str(numbers_drawer_right))
print("Numbers space left   : " + str(numbers_space_left))
print("Numbers space right  : " + str(numbers_space_right))

height_right_column = wo.height_right_column(data_right_column)
#height_warehouse = height_left_column if height_left_column > height_right_column else height_right_column

print("Height left column        : " + str(height_left_column))
print("Height right column       : " + str(height_right_column))
#print("Height automatic warehouse: " + str(height_warehouse))

# Print warehouse; to finish :(
bgc.print_warehouse(data_left_column, data_right_column, height_left_column, height_right_column)

# OLD function
#bash_grap.print_warehouse(height_left,
#                          height_right_upper,
#                          height_drawer_extreme,
#                          height_drawer_left,
#                          height_drawer_right_upper,
#                          numbers_drawer_left,
#                          numbers_drawer_right)

# Check arrays
print(data_left_column)
print(data_right_column)