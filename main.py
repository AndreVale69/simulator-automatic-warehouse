# Default variables
__height_btw_drawers = 25



# Insert all informations of automatic warehouse
print("Insert all informations of automatic warehouse below\n\n")

height_left = int(input("Height left column (meters)          : "))

height_right_upper = int(input("Height right column - Upper (meters) : "))

#height_right_lower = input("Height right column - Lower (meters) : ")


# Insert height of a drawer

height_drawer_extreme = int(input("Height last drawer                   : "))

height_drawer_left = int(input("Height drawer left column            : "))

height_drawer_right_upper = int(input("Height drawer right column           : "))


# Count number of drawers left and right (upper)

# @TODO check negative numbers!

numbers_drawer_left = (height_left - height_drawer_extreme) // (height_drawer_left + __height_btw_drawers)

numbers_drawer_right = (height_right_upper - height_drawer_extreme) // (height_drawer_right_upper + __height_btw_drawers)

print("\nThe number of drawers to the left is  : ", numbers_drawer_left)
print("\nThe number of drawers to the right is : ", numbers_drawer_right)