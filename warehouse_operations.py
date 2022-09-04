from subprocess import check_output
import useful_functions as us_fun
import numpy as np

# Default variables
__height_btw_drawers = 25


# Build a column of warehouse
def column_construction(data_column: np.ndarray, to_compare_data: np.ndarray = np.array([]), is_second: bool = False):
    escape = False
    index = 0
    while escape == False:
        choice = int(input("\nAttention: Don't consider the spaces near the drawers\n"
                        "The current height is: " + str(algorithm_calculate_height(data_column)) + "\n"
                        "Select:\n"
                        "1) Enter 1 empty space (25/space);\n"
                        "2) Enter (input) empty space (25/space);\n"
                        "3) Enter height 1 drawer.\n"
                        "4) Exit.\n"
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
                    if choice == 4:
                        answer = str(input("All information will be lost. Are you sure? [Y/N]: "))
                        if answer  != "N":
                            exit(0)
                        
                    
                    print("ERROR!!! Enter 1, 2 or 3!")

        if is_second:
            res_compare = compare_to_height(data_column, to_compare_data)
            if res_compare == 1:
                raise Exception("The height of right column is grater than left column.")
            else:
                if res_compare == 0:
                    print("Attention! The height of left column is the same of right column")

        print("Now the height is: " + str(algorithm_calculate_height(data_column)))

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
    return algorithm_calculate_height(data_column)


# Calculate height of right column
def height_right_column(data_column: np.ndarray, storage_area: int, buffer_area: int, hole: int):
    height_column = __height_btw_drawers + buffer_area + __height_btw_drawers + storage_area + hole

    height_column = algorithm_calculate_height(data_column, height_column)

    if data_column[0][0] == "Drawer":
        height_column -= __height_btw_drawers

    return height_column


def algorithm_calculate_height(data_column: np.ndarray, height_column: int = 0):
    for i in range(data_column.size):
        if data_column[i][0] == "Space":
            height_column += data_column[i][1]
        else:
            if data_column[i][0] == "Drawer":
                height_column += __height_btw_drawers + data_column[i][1]

    return height_column


def compare_to_height(data_column_1: np.ndarray, data_column_2: np.ndarray):
    longer_length = data_column_1.size if data_column_1.size > data_column_2.size else data_column_2.size

    heigth_left = 0
    heigth_right = 0

    for i in range(longer_length):
        if i < data_column_1.size:
            heigth_left += data_column_1[i][1]
        if i < data_column_2.size:
            heigth_right += data_column_2[i][1]
    
    if heigth_left > heigth_right:
        return 1
    else:
        if heigth_left < heigth_right:
            return -1
        else:
            return 0