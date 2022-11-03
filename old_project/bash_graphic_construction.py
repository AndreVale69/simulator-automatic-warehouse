import numpy as np
import warehouse_operations as wo

def print_warehouse(data_left_column: np.ndarray,
                    data_right_column: np.ndarray,
                    height_left: int,
                    height_right: int):  
    
    # Copy left column array
    tmp_left_column = np.empty_like(data_left_column)
    tmp_left_column[:] = data_left_column
    # Copy right column array
    tmp_right_column = np.empty_like(data_right_column)
    tmp_right_column[:] = data_right_column

    cumulative_height = 0
    index_left = tmp_left_column.size - 1
    index_right = tmp_right_column.size - 1

    # Print top
    print_line(10)
    print_space(10)
    print_line(10, new_line=True)


    # TODO create warehouse print function
    while index_left >= 0:
        if tmp_left_column[index_left][0] == "Space":
            # Print space
            print_slash(new_line=False, is_first=True)
            print_space(8)
            print_slash()
            print_space(10)
            
            index_right = check_right_column(tmp_right_column, index_right)
        else:
            if tmp_left_column[index_left][0] == "Drawer":
                # Print drawer
                print_x()
                print_space(10)
                
                index_right = check_right_column(tmp_right_column, index_right)

        if (tmp_left_column[index_left][1] // 25) > 1:
            tmp_left_column[index_left][1] -= 25
        else:
            index_left -= 1


    # Print botton
    print_stair()


def check_right_column(data_column: np.ndarray, index: int):
    if data_column[index][0] == "Space":
        print_slash()
        print_space(8)
        print_slash(new_line=True)
    else:
        if data_column[index][0] == "Drawer":
            print_x(new_line=True)
        else:
            if data_column[index][0] == "Hole":
                print_space(10, new_line=True)
            else:
                print_x(new_line=True)
    
    #print("Primo: " + str(data_column[index][1]))
    if (data_column[index][1] // 25) > 1:
        data_column[index][1] -= 25
        #print("Secondo: " + str(data_column[index][1]))
    else:
        #print("Terzo: " + str(data_column[index][1]) + "\n")
        index -= 1

    return index
                




def print_line(how_many: int, new_line: bool = False):
    if new_line:
        print("-" * how_many)
    else:
        print("  ", end="")
        print("-" * how_many, end="")


def print_space(how_many: int, new_line: bool = False):
    if new_line:
        print(" " * how_many)
    else:
        print(" " * how_many, end="")


def print_slash(new_line: bool = False, is_first: bool = False):
    if new_line:
        print("|")
    else:
        if is_first:
            print("  ", end="")
            print("|", end="")
        else:
            print("|", end="")


def print_x(new_line: bool = False, how_many: int = 10):
    if new_line:
        print("x" * how_many)
        
    else:
        print("  ", end="")
        print("x" * how_many, end="")


# TODO refactoring the name
def print_stair():
    print("  ", end="")
    print("=" * 30)
    print("  ", end="")
    print("=" * 30)