def print_warehouse(height_left: int,
                    height_right_upper: int,
                    height_drawer_extreme: int,
                    height_drawer_left: int,
                    height_drawer_right_upper: int,
                    numbers_drawer_left: int,
                    numbers_drawer_right: int):
    print_line(10)
    print_space(10)
    print_line(10, True)

    print_slash()
    print_space(8)
    print_slash()
    print_space(10)
    print_slash()
    print_space(8)
    print_slash()


def print_line(how_many, new_line: bool = False):
    if new_line:
        print("-" * how_many)
    else:
        print("-" * how_many, end="")


def print_space(how_many):
    print(" " * how_many, end="")


def print_slash():
    print("|", end="")
