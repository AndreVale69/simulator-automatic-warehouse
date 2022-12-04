import copy
from src.material import Material


class Drawer:
    def __init__(self, items: list = None):
        from src.useful_func import obt_value_json

        # items inside the drawer
        if items is None:
            items = []
        self.items = copy.deepcopy(items)
        self.def_space = obt_value_json("default_height_space")
        self.__calculate_max_height()

        self.best_x = None
        self.best_y = None

    def __eq__(self, other):
        """Overrides the default implementation"""
        # TODO check
        return isinstance(other,
                          Drawer) and self.get_items() == other.get_items() and self.get_max_height() == other.get_max_height() and self.get_max_num_space() == other.get_max_num_space()

    def __hash__(self):
        """Overrides the default implementation"""
        # TODO check
        return 13 ^ hash(self.get_items()) ^ hash(self.get_max_height()) ^ hash(self.get_max_num_space())

    def __deepcopy__(self, memo):
        newone = type(self)(self.get_items())
        newone.__dict__.update(self.__dict__)
        self.items = copy.deepcopy(self.get_items(), memo)
        return newone

    def get_items(self) -> list[Material]:
        return self.items

    def add_material(self, material: Material):
        # insert in tail
        self.items.append(material)
        self.__calculate_max_height()

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

    def get_best_x(self) -> int:
        return self.best_x

    def get_best_y(self) -> int:
        return self.best_y

    def set_best_x(self, pos_x: int):
        self.best_x = pos_x

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
            self.max_height = None
            self.num_space = None
