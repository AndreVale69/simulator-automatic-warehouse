from src.material import Material


class Drawer:
    def __init__(self, items: list = None):
        # items inside the drawer
        if items is None:
            items = []
        self.__items = items.copy()
        self.__calculate_max_height()

    def __eq__(self, other):
        """Overrides the default implementation"""
        # TODO check
        return isinstance(other,
                          Drawer) and self.get_items() == other.get_items() and self.get_max_height() == other.get_max_height() and self.get_max_num_space() == other.get_max_num_space()

    def __hash__(self):
        """Overrides the default implementation"""
        # TODO check
        return 13 ^ hash(self.get_items()) ^ hash(self.get_max_height()) ^ hash(self.get_max_num_space())

    def get_items(self):
        return self.__items

    def add_material(self, material: Material):
        # insert in tail
        self.__items.append(material)
        self.__calculate_max_height()

    def get_max_height(self) -> int:
        """
        :return: maximum height of a material inside drawer
        """
        return self.__max_height

    def get_max_num_space(self) -> int:
        """
        :return: number of occupied spaces in the warehouse
        """
        return self.__num_space

    # private method to calculate maximum height of a drawer
    def __calculate_max_height(self):
        from src.useful_func import obt_value_json
        def_space = obt_value_json("default_height_space")

        try:
            # set tmp max to first element
            tmp_max_height = Material.get_height(self.__items[0])

            # search max
            for i in range(1, len(self.__items)):
                height = Material.get_height(self.__items[i])

                if height > tmp_max_height:
                    tmp_max_height = height

            # save max height
            # maximum height of a drawer based on the elements present
            self.__max_height = tmp_max_height

            # Check if is even or odd
            if (self.__max_height % def_space) == 0:
                # even
                self.__num_space = self.__max_height // def_space
            else:
                # odd, approx the next
                self.__num_space = (self.__max_height // def_space) + 1
        except IndexError as e:
            self.__max_height = None
            self.__num_space = None
