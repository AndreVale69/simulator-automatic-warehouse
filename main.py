#from inspect import indentsize     TODO REMOVE!
#from operator import countOf       TODO REMOVE!
import numpy as np
import useful_functions as us_fun
import bash_graphic_construction as bash_grap

# Default variables
__height_btw_drawers = 25
__height_space = 50

# Contains the measurements of the size of the drawers
type = np.dtype([("name", "U30"), ("height", "uint32")])
data_left_column = np.array([], dtype=type)
data_right_column = np.array([], dtype=type)

# Insert all information of automatic warehouse
print("Enter all information of automatic warehouse below\n\n")

print("Create left column...\n")
us_fun.column_construction(data_left_column)

print("Create right column...\n")
us_fun.column_construction(data_right_column)

print(data_left_column)
print(data_right_column)

# Count number of drawers left
#for i in data_left_column:
    #if data_left_column[i] == 
    #numbers_drawer_left = 

#height_left = us_fun.check_negative_value("Height left column (meters)          : ")
#height_right_upper = us_fun.check_negative_value("Height right column - Upper (meters) : ")
# Insert height of a drawer
#height_drawer_extreme = us_fun.check_negative_value("Height last drawer                   : ")
#height_drawer_left = us_fun.check_negative_value("Height drawer left column            : ")
#height_drawer_right_upper = us_fun.check_negative_value("Height drawer right column           : ")

# TODO check height drawer is lower thank height_left

# Count number of drawers left and right (upper)
#numbers_drawer_left = (height_left - height_drawer_extreme) // \
#                      (height_drawer_left + __height_btw_drawers)

#numbers_drawer_right = (height_right_upper - height_drawer_extreme) // \
#                       (height_drawer_right_upper + __height_btw_drawers)

#print("\nThe number of drawers to the left is  : ", numbers_drawer_left)
#print("\nThe number of drawers to the right is : ", numbers_drawer_right)

#bash_grap.print_warehouse(height_left,
#                          height_right_upper,
#                          height_drawer_extreme,
#                          height_drawer_left,
#                          height_drawer_right_upper,
#                          numbers_drawer_left,
#                          numbers_drawer_right)
