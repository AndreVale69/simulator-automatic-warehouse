from src.drawer import Drawer
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


class Carousel(DrawerContainer):
    def __init__(self, info: dict):
        super().__init__(0)

        # get first y to start
        first_y = self.get_height_col() + self.get_hole()

        # create container
        for i in range(self.get_deposit() + self.get_buffer()):
            self.add_item_to_container(EmptyEntry(0, i + first_y))

    def __deepcopy__(self, memo):
        return super().__deepcopy__(memo)

    # override
    def add_drawer(self, to_show: bool, drawer: Drawer) -> bool:
        """
        Add a drawer in buffer area or show as an output.

        :param to_show: True to show a drawer, otherwise False to put it into buffer area
        :param drawer: To show or to save
        :return: True there is space and the operation is successes, False there isn't space and the operation is failed
        """
        store = self.get_height_col()
        hole = self.get_hole()
        dep = self.get_deposit()
        first_y = store + hole
        if to_show:
            # check if it's empty
            if isinstance(self.get_container()[0], EmptyEntry):
                drawer_entry = self.__create_drawerEntry(drawer, first_y, 0)
                # connect Entry to Drawer
                drawer.set_first_drawerEntry(drawer_entry)
                for i in range(1, dep):
                    self.__create_drawerEntry(drawer, first_y, i)
                return True
            else:
                return False
        else:
            if isinstance(self.get_container()[dep], EmptyEntry):
                drawer_entry = self.__create_drawerEntry(drawer, first_y, dep)
                # connect Entry to Drawer
                drawer.set_first_drawerEntry(drawer_entry)
                dep += 1
                for i in range(dep, len(self.get_container())):
                    self.__create_drawerEntry(drawer, first_y, i)
                return True
            else:
                return False

    def __create_drawerEntry(self, drawer: Drawer, first_y: int, index: int) -> DrawerEntry:
        # initialize positions
        drawer_entry = DrawerEntry(self.get_pos_x(), first_y + index)
        # connect Drawer to entry
        drawer_entry.add_drawer(drawer)
        # add to container
        self.get_container()[index] = drawer_entry
        # return the drawer entry just added
        return drawer_entry

    # override
    def remove_drawer(self, drawer: Drawer):
        super().remove_drawer(drawer)
