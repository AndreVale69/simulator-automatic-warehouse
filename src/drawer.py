from src.material import Material


class Drawer:
    # items inside the drawer
    __items = []
    # maximum height of a drawer based on the elements present
    __max_height = 0
    # number of occupied spaces in the warehouse
    __num_space = 0

    def __init__(self, items: list = None):
        if items is not None:
            self.__items = items.copy()
            self.__calculate_max_height()

    def add_material(self, material: Material):
        # insert in tail
        self.__items.append(material)
        self.__calculate_max_height()

    def get_max_height(self):
        if len(self.__items) == 0:
            return 0
        else:
            return self.__max_height

    def get_max_num_space(self):
        return self.__num_space

    # private method to calculate maximum height of a drawer
    def __calculate_max_height(self):
        # set max to first element
        tmp_max_height = Material.get_height(self.__items[0])

        # search max
        for i in range(1, len(self.__items)):
            height = Material.get_height(self.__items[i])

            if height > tmp_max_height:
                tmp_max_height = height

        # save max height
        self.__max_height = tmp_max_height

        # Check if is even or odd
        if (self.__max_height % 25) == 0:
            # even
            self.__num_space = self.__max_height // 25
        else:
            # odd, approx the next
            self.__num_space = (self.__max_height // 25) + 1

    # TODO: debug
    def print_array(self):
        for i in range(len(self.__items)):
            print(Material.get_barcode(self.__items[i]))
            print(Material.get_name(self.__items[i]))
            print(Material.get_height(self.__items[i]))
            print(Material.get_length(self.__items[i]))
            print(Material.get_width(self.__items[i]))