import useful_functions as us_fun
import numpy as np

# Default variables
__height_btw_drawers = 25


# Build a column of warehouse
def column_construction(data_column: np.ndarray):
    escape = False
    index = 0
    while escape == False:
        choice = int(input("\nAttention: Don't consider the spaces near the drawers\n"
                        "Select:\n"
                        "1) Enter 1 empty space (25/space);\n"
                        "2) Enter (input) empty space (25/space);\n"
                        "3) Enter height 1 drawer.\n"
                        "Choice: "))
        if choice == 1:
            data_column = np.insert(data_column, index, ("Space", __height_btw_drawers))
            index += 1
        else:
            if choice == 2:
                how_many = us_fun.check_negative_value("Enter the number of blanks: ")
                for i in range(how_many):
                    data_column = np.insert(data_column, index, ("Space", __height_btw_drawers))
                    index += 1
            else:
                if choice == 3:
                    while True:
                        height_drawer = us_fun.check_negative_value("Enter the height of a drawer: ")
                        if (height_drawer % __height_btw_drawers) != 0:
                            print("\nPlease enter a multiple of 25!!!\n")
                        else:
                            break
                    
                    data_column = np.insert(data_column, index, ("Drawer", height_drawer))
                    index += 1
                else:
                    print("ERROR!!! Enter 1, 2 or 3!")

        answer = str(input("Continue? [Y/N] "))
        escape = us_fun.check_answer(answer)
    
    return data_column


# Count number of drawers
def count_drawers(data_column: np.ndarray):
    numbers_drawer = 0

    for i in range(data_column.size):
        if data_column[i][0] == "Drawer":
            numbers_drawer += 1

    return numbers_drawer


# Count number of space
def count_space(data_column: np.ndarray):
    numbers_space = 0

    for i in range(data_column.size):
        if data_column[i][0] == "Space":
            numbers_space += 1

    return numbers_space


# Calculate height of left column
def height_left_column(data_column: np.ndarray):
    height_column = __height_btw_drawers

    for i in range(data_column.size):
        if data_column[i][0] == "Space" and data_column[i + 1][0] == "Space":
            height_column += data_column[i][1]
        else:
            height_column += __height_btw_drawers + data_column[i][1]

    return height_column


# Calculate height of right column
def height_right_column(data_column: np.ndarray, storage_area: int, buffer_area: int, hole: int):
    height_column = __height_btw_drawers + buffer_area + __height_btw_drawers + storage_area + hole
    

    for i in range(data_column.size):
        if data_column[i][0] == "Space" and data_column[i + 1][0] == "Space":
            height_column += data_column[i][1]
        else:
            height_column += __height_btw_drawers + data_column[i][1]

    return height_column
