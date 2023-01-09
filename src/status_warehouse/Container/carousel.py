from src.drawer import Drawer
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.status_warehouse.Entry.emptyEntry import EmptyEntry


class Carousel(DrawerContainer):
    def __init__(self, info: dict):
        height_carousel = info["deposit_height"] + info["buffer_height"]
        super().__init__(height_carousel, info["x_offset"], info["width"])

        # get first y to start
        first_y = self.get_height_col() + self.get_hole()

        # create container with only two positions
        # create deposit
        self.create_new_space(EmptyEntry(self.get_offset_x(), first_y))
        # create buffer
        self.create_new_space(EmptyEntry(self.get_offset_x(), first_y + (self.get_deposit() + self.get_buffer())))

    def __deepcopy__(self, memo):
        return super().__deepcopy__(memo)

    # override
    def add_drawer(self, drawer: Drawer, index: int = None) -> bool:
        """
        Add a drawer in buffer area or show as an output.

        :param index: None
        :param drawer: To show or to save
        :return: True there is space and the operation is successes, False there isn't space and the operation is failed
        """
        store = self.get_height_col()
        hole = self.get_hole()
        dep = self.get_deposit()
        first_y = store + hole

        # TODO: rmv to_show controllare solo deposit else buffer
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
                return False

    def create_drawerEntry(self, drawer: Drawer, first_y: int, is_buffer: bool):
        # initialize positions
        drawer_entry = DrawerEntry(self.get_offset_x(), first_y + (self.get_deposit() + self.get_buffer())) \
                        if is_buffer else DrawerEntry(self.get_offset_x(), first_y)
        # connect Drawer to entry
        drawer_entry.add_drawer(drawer)
        # add to container
        self.get_container()[int(is_buffer)] = drawer_entry
        # connect Entry just added to relative Drawer
        drawer.set_first_drawerEntry(drawer_entry)

    # override
    def remove_drawer(self, drawer: Drawer):
        super().remove_drawer(drawer)
