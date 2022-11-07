from src.useful_func import read_value_of_const_json
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.drawer import Drawer


class Column(DrawerContainer):
    def __init__(self, height: int):
        super().__init__(height)

    # override
    def check_minimum_space(self, drawer: Drawer) -> list:
        min_space = self.get_height()
        count = 0
        start_index = 0
        num_space = drawer.get_max_num_space()
        container = self.get_container()

        for i in range(len(container) + 1):
            if i != len(container):
                # count number of space
                if isinstance(container[i], type(EmptyEntry())):
                    count = count + 1
                else:
                    # otherwise, if its minimum and there is enough space
                    if (count < min_space) & (count >= num_space):
                        min_space = count
                        start_index = i - count
                    # restart the count with reset
                    count = 0
            else:
                if (count < min_space) & (count >= num_space):
                    min_space = count
                    start_index = i - count
                # restart the count with reset
                count = 0  # TODO: check eventually rmv

        print("Min space & index: " + str(min_space) + " ; " + str(start_index))

        # if warehouse is empty
        if min_space == self.get_height():
            # double security check
            for i in range(len(container)):
                # if it isn't empty
                if isinstance(container[i], Drawer):
                    # raise IndexError("There isn't any space for this drawer.")
                    print("A")
                    return [-1, -1]
            min_space = len(container)

        # alloc only minimum space
        if min_space > num_space:
            min_space = num_space
        else:
            # otherwise there isn't any space
            if min_space < num_space:
                # raise IndexError("There isn't any space for this drawer.")
                return [-1, -1]

        return [min_space, start_index]

    # override
    def add_drawer(self, index: int, drawer: Drawer):
        how_many = drawer.get_max_num_space()

        while how_many > 0:
            self.get_container()[index] = drawer
            index += 1
            how_many -= 1

    # override
    def remove_drawer(self, drawer: Drawer):
        for i in range(len(self.get_container())):
            if self.get_container()[i] is drawer:
                self.get_container()[i] = EmptyEntry()
