from inspect import indentsize
from operator import countOf
import numpy as np
import useful_functions as us_fun
import bash_graphic_construction as bash_grap

# Default variables
__height_btw_drawers = 25
__height_space = 50

# Insert all information of automatic warehouse
print("Enter all information of automatic warehouse below\n\n")

print("Create left column...\n\n")

# Contains the measurements of the size of the drawers
type = np.dtype([("name", "U30"), ("height", "uint32")])
data_left_column = np.array([], dtype=type)

escape = False
index = 0
while escape == False:
    print (index)
    choice = int(input("\nSelect:\n"
                       "1) Enter 1 empty space (50/space);\n"
                       "2) Enter (input) empty space (50/space);\n"
                       "3) Enter height 1 drawer.\n"
                       "Choice: "))
    if choice == 1:
        data_left_column = np.insert(data_left_column, index, ("Space", __height_space))
        index += 1
    else:
        if choice == 2:
            how_many = us_fun.check_negative_value("Enter the number of blanks: ")
            for i in range(how_many):
                data_left_column = np.insert(data_left_column, index, ("Space", __height_space))
                index += 1
        else:
            if choice == 3:
                height_drawer = us_fun.check_negative_value("Enter the height of a drawer: ")
                data_left_column = np.insert(data_left_column, index, ("Drawer", height_drawer))
                index += 1
            else:
                print("ERROR!!! Enter 1, 2 or 3!")

    answer = str(input("Continue? [Y/N] "))
    escape = us_fun.check_answer(answer)

print(data_left_column)

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
