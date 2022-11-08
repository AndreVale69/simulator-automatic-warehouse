from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.drawer import Drawer


class Column(DrawerContainer):
    def __init__(self, height: int, pos_y: int):
        super().__init__(height, pos_y)

    def check_minimum_space(self, max_space: int) -> list:
        min_space = self.get_height()
        count = 0
        start_index = 0
        container = self.get_container()

        ############################
        # Minimum search algorithm #
        ############################
        for i in range(len(container) + 1):
            if i != len(container):
                # count number of space
                if isinstance(container[i], EmptyEntry):
                    count = count + 1
                else:
                    # otherwise, if its minimum and there is enough space
                    if (count < min_space) & (count >= max_space):
                        min_space = count
                        start_index = i - count
                    # restart the count with reset
                    count = 0
            else:
                if (count < min_space) & (count >= max_space):
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
        if min_space > max_space:
            min_space = max_space
        else:
            # otherwise there isn't any space
            if min_space < max_space:
                # raise IndexError("There isn't any space for this drawer.")
                return [-1, -1]

        return [min_space, start_index]

    # override
    def add_drawer(self, index: int, drawer: Drawer):
        how_many = drawer.get_max_num_space()

        while how_many > 0:
            # initialize positions
            drawer_entry = DrawerEntry(index, super().get_pos_y())
            # connect Drawer to entry
            drawer_entry.add_drawer(drawer)
            # add to container
            self.get_container()[index] = drawer_entry
            index += 1
            how_many -= 1

    # override
    def remove_drawer(self, drawer: Drawer):
        super().remove_drawer(drawer)
