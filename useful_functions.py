from array import array
import main as m
import numpy as np


# check if the enter value is positive
def check_negative_value(string_to_print):
    while True:
        value = int(input(string_to_print))

        if value <= 0:
            print("Please try to digit a positive value!\n")
        else:
            break

    return value


# check if the answer is Y or N, otherwise error
def check_answer(answer: str):
    escape = False

    while True:
        if answer == "N":
            escape = True
            break
        else:
            if answer != "Y":
                answer = str(input("Enter only Y or N if you wanna continue or no! Continue? [Y/N] "))
            else:
                break

    return escape


# build a column of warehouse
def column_construction(data_column: array):
    escape = False
    index = 0
    while escape == False:
        choice = int(input("\nSelect:\n"
                        "1) Enter 1 empty space (50/space);\n"
                        "2) Enter (input) empty space (50/space);\n"
                        "3) Enter height 1 drawer.\n"
                        "Choice: "))
        if choice == 1:
            data_column = np.insert(data_column, index, ("Space", m.__height_space))
            index += 1
        else:
            if choice == 2:
                how_many = check_negative_value("Enter the number of blanks: ")
                for i in range(how_many):
                    data_column = np.insert(data_column, index, ("Space", m.__height_space))
                    index += 1
            else:
                if choice == 3:
                    height_drawer = check_negative_value("Enter the height of a drawer: ")
                    data_column = np.insert(data_column, index, ("Drawer", height_drawer))
                    index += 1
                else:
                    print("ERROR!!! Enter 1, 2 or 3!")

        answer = str(input("Continue? [Y/N] "))
        escape = check_answer(answer)
    
    return data_column