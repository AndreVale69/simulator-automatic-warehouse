import numpy as np

def print_warehouse(data_left_column: np.ndarray, data_right_column: np.ndarray):
    index_left = data_left_column.size
    index_right = data_right_column.size

    # TODO create warehouse print function
    while True:
        if data_left_column[index_left][0] == "Space":
            # Print space
            print()
        else:
            if data_left_column[index_left][0] == "Drawer":
                # Print drawer
                print()
            else:
                if data_column[index][0] == "Hole":
                    # Print hole
                    print()
                else:
                    # Print drawer
                    print()
        

            

    print_line(10)
    print_space(10)
    print_line(10, True)

    #for i in range(height_drawer_extreme // 100):
    #    print_slash(False, numbers_drawer_left - i)
    #    print_space(8)
    #    print_slash()

    print_line(10)

    # print_space(10)
    # print_slash()
    # print_space(8)
    # print_slash()


def print_line(how_many, new_line: bool = False):
    if new_line:
        print("-" * how_many)
    else:
        print("  ", end="")
        print("-" * how_many, end="")


def print_space(how_many):
    print(" " * how_many, end="")


def print_slash(new_line: bool = False, value: int = 0):
    if new_line:
        print("|")
    else:
        if value != 0:
            print("  ", end="")
            print("|", end="")
        else:
            print("  ", end="")
            print("|", end="")
