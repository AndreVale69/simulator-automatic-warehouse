from src.material import Material


class Drawer:
    def __init__(self, items: list = None):
        # items inside the drawer
        self.__items = items.copy()
        self.__calculate_max_height()

    def add_material(self, material: Material):
        # insert in tail
        self.__items.append(material)
        self.__calculate_max_height()

    def get_max_height(self) -> int:
        """
        :return: maximum height of a material inside drawer
        """
        if len(self.__items) == 0:
            return 0
        else:
            return self.__max_height

    def get_max_num_space(self) -> int:
        """
        :return: number of occupied spaces in the warehouse
        """
        if len(self.__items) == 0:
            return 0
        else:
            return self.__num_space

    # private method to calculate maximum height of a drawer
    def __calculate_max_height(self):
        from src.useful_func import obt_value_json
        def_space = obt_value_json("default_height_space")

        # set max to first element
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
