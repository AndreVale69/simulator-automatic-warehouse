from src.useful_func import read_value_of_const_json
from status_warehouse.Container.drawerContainer import DrawerContainer
from status_warehouse.Entry.outputEntry import OutputEntry
from status_warehouse.Entry.drawerEntry import DrawerEntry
from status_warehouse.Entry.emptyEntry import EmptyEntry


class Column(DrawerContainer):
    def __init__(self, height: int):
        super().__init__(height)
        self.__col_left = []
        self.__col_right = []
        def_space = read_value_of_const_json("default_height_space")
        height_deposit = read_value_of_const_json("deposit_height") // def_space
        height_hole = read_value_of_const_json("hole_height") // def_space

        # create left and right column
        for i in range(super().get_num_entries()):
            # left
            self.__col_left.append(EmptyEntry())

            # right
            if i >= height_deposit & i < height_hole:
                # Output space
                self.__col_right.append(OutputEntry())
            else:
                # Empty space
                self.__col_right.append(EmptyEntry())

    def get_left(self) -> list:
        return self.__col_left

    def get_right(self) -> list:
        return self.__col_right

    # override
    def add_drawer(self):
        print("add")

    # override
    def remove_drawer(self):
        print("remove")
