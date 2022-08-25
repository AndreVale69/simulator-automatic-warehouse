import useful_functions as us_fun
import bash_graphic_construction as bash_grap

# Default variables
__height_btw_drawers = 25

# Insert all information of automatic warehouse
print("Insert all informations of automatic warehouse below\n\n")

height_left = us_fun.check_negative_value("Height left column (meters)          : ")
height_right_upper = us_fun.check_negative_value("Height right column - Upper (meters) : ")
# Insert height of a drawer
height_drawer_extreme = us_fun.check_negative_value("Height last drawer                   : ")
height_drawer_left = us_fun.check_negative_value("Height drawer left column            : ")
height_drawer_right_upper = us_fun.check_negative_value("Height drawer right column           : ")

# TODO check height drawer is lower thank height_left

# Count number of drawers left and right (upper)
numbers_drawer_left = (height_left - height_drawer_extreme) // \
                      (height_drawer_left + __height_btw_drawers)

numbers_drawer_right = (height_right_upper - height_drawer_extreme) // \
                       (height_drawer_right_upper + __height_btw_drawers)

print("\nThe number of drawers to the left is  : ", numbers_drawer_left)
print("\nThe number of drawers to the right is : ", numbers_drawer_right)

bash_grap.print_warehouse(height_left,
                          height_right_upper,
                          height_drawer_extreme,
                          height_drawer_left,
                          height_drawer_right_upper,
                          numbers_drawer_left,
                          numbers_drawer_right)
