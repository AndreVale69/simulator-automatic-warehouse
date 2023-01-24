import copy
import random

from src.material import Material


class Drawer:
    def __init__(self, items: list = None):
        from src.useful_func import open_config

        # items inside the drawer
        config: dict = open_config()

        if items is None:
            items = []
        self.items = copy.deepcopy(items)
        self.def_space = config["default_height_space"]
        self.__calculate_max_height()

        self.first_drawerEntry = None
        self.best_offset_x = None
        self.best_y = None

    def __eq__(self, other):
        """Overrides the default implementation"""
        return isinstance(other, Drawer) and \
            self.get_items() == other.get_items() and \
            self.get_max_height() == other.get_max_height() and \
            self.get_max_num_space() == other.get_max_num_space() and \
            self.get_first_drawerEntry() == other.get_first_drawerEntry()

    def __hash__(self):
        """Overrides the default implementation"""
        return 13 ^ hash(self.get_items()) ^ hash(self.get_max_height()) ^ hash(self.get_max_num_space())

    def __deepcopy__(self, memo):
        copy_obj = Drawer(self.get_items())
        copy_obj.items = copy.deepcopy(self.get_items(), memo)
        copy_obj.def_space = self.__get_def_space()
        copy_obj.max_height = self.get_max_height()
        copy_obj.num_space = self.get_max_num_space()
        copy_obj.first_drawerEntry = self.get_first_drawerEntry()
        copy_obj.best_offset_x = self.get_best_offset_x()
        copy_obj.best_y = self.get_best_y()
        return copy_obj

    def get_items(self) -> list[Material]:
        return self.items

    def get_max_height(self) -> int:
        """
        :return: maximum height of a material inside drawer
        """
        return self.max_height

    def get_max_num_space(self) -> int:
        """
        :return: number of occupied spaces in the warehouse
        """
        return self.num_space

    def get_first_drawerEntry(self):
        return self.first_drawerEntry

    def get_best_offset_x(self) -> int:
        return self.best_offset_x

    def get_best_y(self) -> int:
        return self.best_y

    def get_num_materials(self) -> int:
        return len(self.items)

    def add_material(self, material: Material):
        # insert in tail
        self.items.append(material)
        self.__calculate_max_height()

    def set_first_drawerEntry(self, drawer_entry):
        self.first_drawerEntry = drawer_entry

    def set_best_offset_x(self, offset_x: int):
        self.best_offset_x = offset_x

    def set_best_y(self, pos_y: int):
        self.best_y = pos_y

    def __get_def_space(self) -> int:
        return self.def_space

    # private method to calculate maximum height of a drawer
    def __calculate_max_height(self):
        def_space = self.__get_def_space()

        try:
            # set tmp max to first element
            tmp_max_height = self.get_items()[0].get_height()

            # search max
            for i in range(1, len(self.items)):
                height = self.get_items()[i].get_height()

                if height > tmp_max_height:
                    tmp_max_height = height

            # save max height
            # maximum height of a drawer based on the elements present
            self.max_height = tmp_max_height

            # Check if is even or odd
            if (self.max_height % def_space) == 0:
                # even
                self.num_space = self.max_height // def_space
            else:
                # odd, approx the next
                self.num_space = (self.max_height // def_space) + 1
        except IndexError:
            self.max_height = def_space
            self.num_space = self.max_height // def_space


def gen_rand_drawers(how_many: int, materials_to_insert: list[Material]) -> list[Drawer]:
    drawers: list[Drawer] = []
    for i in range(how_many):
        # select a random material
        rand_index = random.randint(0, len(materials_to_insert) - 1)
        # create a random drawer with a random material
        drawers.append(Drawer([materials_to_insert[i]]))
        # remove the material just added
        materials_to_insert.remove(materials_to_insert[rand_index])
    # if there are some materials yet
    while len(materials_to_insert) != 0:
        # select a random material
        rand_index_mat = random.randint(0, len(materials_to_insert) - 1)
        rand_index_draw = random.randint(0, len(drawers) - 1)
        # add random material inside a random drawer
        drawers[rand_index_draw].add_material(materials_to_insert[rand_index_mat])
        # remove the material just added
        materials_to_insert.remove(materials_to_insert[rand_index_mat])
    return drawers
