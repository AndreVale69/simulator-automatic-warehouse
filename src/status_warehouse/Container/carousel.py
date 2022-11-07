from src.useful_func import obt_value_json
from src.drawer import Drawer
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Entry.emptyEntry import EmptyEntry


class Carousel(DrawerContainer):
    def __init__(self, height: int):
        super().__init__(height)

    # override
    def add_drawer(self, to_show: bool, drawer: Drawer) -> bool:
        """
        Add a drawer in buffer area or show as an output.

        :param to_show: True to show a drawer, otherwise False to put it into buffer area
        :param drawer: To show or to save
        :return: True there is space and the operation is successes, False there isn't space and the operation is failed
        """
        def_space = obt_value_json("default_height_space")
        buffer = obt_value_json("buffer_height") // def_space
        hole = obt_value_json("hole_height") // def_space
        if to_show:
            # check if it's empty
            if isinstance(self.get_container()[0], type(EmptyEntry())):
                for i in range(buffer):
                    self.get_container()[i] = drawer
                return True
            else:
                return False
        else:
            if isinstance(self.get_container()[buffer], type(EmptyEntry())):
                for i in range(buffer, hole + buffer):
                    self.get_container()[i] = drawer
                return True
            else:
                return False

    # override
    def remove_drawer(self, drawer: Drawer):
        super().remove_drawer(drawer)
