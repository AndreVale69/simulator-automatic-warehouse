import copy

from src.sim.drawer import Drawer
from src.sim.status_warehouse.container.drawer_container import DrawerContainer
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry


class Carousel(DrawerContainer):
    def __init__(self, info: dict, warehouse):
        height_carousel = info["deposit_height"] + info["buffer_height"]
        super().__init__(height_carousel, info["x_offset"], info["width"], warehouse)

        # get first y to start
        first_y = self.get_height_col() + self.get_hole()

        # create container with only two positions
        # create deposit
        self.create_new_space(EmptyEntry(self.get_offset_x(), first_y))
        # create buffer
        self.create_new_space(EmptyEntry(self.get_offset_x(), first_y + (self.get_deposit() + self.get_buffer())))

    def __deepcopy__(self, memo):
        info: dict = {
            "deposit_height": self.get_deposit() * self.get_def_space(),
            "buffer_height": self.get_buffer() * self.get_def_space(),
            "x_offset": self.get_offset_x(),
            "width": self.get_width()
        }
        copy_obj = Carousel(info, self.get_warehouse())
        copy_obj.container = copy.deepcopy(self.get_container(), memo)
        return copy_obj

    def get_deposit_entry(self) -> DrawerEntry | EmptyEntry:
        return self.get_container()[0]

    def get_buffer_entry(self) -> DrawerEntry | EmptyEntry:
        return self.get_container()[1]

    def get_num_drawers(self) -> int:
        """How many drawers there are"""
        count = 0
        if type(self.get_deposit_entry()) is DrawerEntry:
            count += 1
        if type(self.get_buffer_entry()) is DrawerEntry:
            count += 1
        return count

    def is_buffer_full(self) -> bool:
        """
        Check the buffer
        :return: True if is full, False otherwise
        """
        # check if the first position of buffer have a Drawer
        return True if type(self.get_buffer_entry()) is DrawerEntry else False

    def is_deposit_full(self) -> bool:
        """
        Check the deposit
        :return: True if is full, False otherwise
        """
        # check if the first position of deposit have a Drawer
        return True if type(self.get_deposit_entry()) is DrawerEntry else False

    # override
    def add_drawer(self, drawer: Drawer, index: int = None) -> bool:
        """
        Add a drawer in buffer area or show as an output.

        :param index: None
        :param drawer: To show or to save
        :return: True there is space and the operation is successes, False there isn't space and the operation is failed
        """
        deposit = self.get_deposit()
        store = self.get_height_col()
        hole = self.get_hole()
        first_y = store + hole + deposit

        # check if it's empty the deposit
        if isinstance(self.get_container()[0], EmptyEntry):
            self.create_drawerEntry(drawer, first_y, is_buffer=False)
            return True
        else:
            # otherwise, check if it's empty the buffer
            if isinstance(self.get_container()[1], EmptyEntry):
                self.create_drawerEntry(drawer, first_y, is_buffer=True)
                return True
            else:
                raise RuntimeError("Collision!")

    def create_drawerEntry(self, drawer: Drawer, first_y: int, is_buffer: bool):
        # initialize positions
        drawer_entry = DrawerEntry(self.get_offset_x(), first_y + self.get_buffer()) if is_buffer \
                  else DrawerEntry(self.get_offset_x(), first_y)
        # connect Drawer to entry
        drawer_entry.add_drawer(drawer)
        # add to container
        self.get_container()[int(is_buffer)] = drawer_entry
        # connect Entry just added to relative Drawer
        drawer.set_first_drawerEntry(drawer_entry)

    # override
    def remove_drawer(self, drawer: Drawer) -> bool:
        """Remove a drawer"""
        # return super().remove_drawer(drawer)
        first_entry: DrawerEntry = drawer.get_first_drawerEntry()
        entry_y_to_rmv: int = first_entry.get_pos_y()
        entry_x_to_rmv: int = first_entry.get_offset_x()

        for index, entry in enumerate(self.get_container()):
            if entry.get_pos_y() == entry_y_to_rmv:
                self.get_container()[index] = EmptyEntry(entry_x_to_rmv, entry_y_to_rmv)
                return True
        return False
