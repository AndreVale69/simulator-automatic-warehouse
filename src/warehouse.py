from src.drawer import Drawer
from src.material import Material
from src.useful_func import obt_value_json
from src.status_warehouse.Container.drawerContainer import DrawerContainer
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Container.carousel import Carousel


class Warehouse:
    __warehouse_left = []
    __warehouse_right = []

    def __init__(self):
        self.__height = obt_value_json("height_warehouse")

        # TODO: to rmv DEBUG
        # material = Material(123, "name", 256, 789, 12345)
        # material2 = Material(234, "abc", 126, 987, 00000)
        # drawer = Drawer([material, material2])
        # material3 = Material(567, "def", 128, 564, 0)
        # drawer2 = Drawer([material3])

        # container_left = Column(self.__height)
        # container_left.add_drawer(0, drawer)
        # print("------------------------------------------------------")
        # print(container_left.get_container())
        # print("------------------------------------------------------")

        # print(container_left.check_minimum_space(drawer2))

        # container_left.remove_drawer(drawer)

        # print("------------------------------------------------------")
        # print(container_left.get_container())
        # print("------------------------------------------------------")

        # print(container_left.check_minimum_space(drawer2))

        # container_left = Carousel(self.__height)
        # container_left.add_drawer(True, drawer)
        # print("------------------------------------------------------")
        # print(container_left.get_container())
        # print("------------------------------------------------------")

        # container_left.remove_drawer(drawer)

        # print("------------------------------------------------------")
        # print(container_left.get_container())
        # print("------------------------------------------------------")

        # container_left.add_drawer(False, drawer2)

        # print("------------------------------------------------------")
        # print(container_left.get_container())
        # print("------------------------------------------------------")

        # TODO: opt this class
        # creation of space left
        num_space_left = self.__height // 25
        for i in range(num_space_left):
            self.__warehouse_left.append(25)

        # creation of space right
        height_dep = obt_value_json("deposit_height")
        height_bs = obt_value_json("buffer_height")

        # buffer area
        self.__warehouse_right.append(height_bs // 2)
        # storage area
        self.__warehouse_right.append(height_bs // 2)
        num_space_right = height_dep // 25
        for i in range(num_space_right):
            self.__warehouse_right.append(25)

    def set_height(self, height: int):
        self.__height = height

    def get_height(self) -> int:
        return self.__height

    def get_warehouse(self) -> []:
        return self.__warehouse_left

    def add_drawer(self, drawer: Drawer):
        is_left = False

        min_left = self.__count_minimum_space(drawer.get_max_num_space(), self.__warehouse_left)
        warehouse_right_col = self.__warehouse_right.copy()
        warehouse_right_col.pop(0)
        warehouse_right_col.pop(0)
        min_right = self.__count_minimum_space(drawer.get_max_num_space(), warehouse_right_col)

        if isinstance(min_left, list) & isinstance(min_right, list):
            if min_left[0] <= min_right[0]:
                tmp_arr = min_left.copy()
                is_left = True
            else:
                tmp_arr = min_right.copy()
        else:
            if isinstance(min_left, list):
                tmp_arr = min_left.copy()
                is_left = True
            else:
                if isinstance(min_right, list):
                    tmp_arr = min_right.copy()
                else:
                    raise IndexError("There isn't any space for this drawer.")
        # Help
        #   tmp_arr:
        #           temp_arr[0] = min_space   --> numbers of elements to remove
        #           temp_arr[1] = start_index --> start index on __warehouse list

        # insert element
        if is_left:
            self.__warehouse_left[tmp_arr[1]] = drawer
            tmp_arr[1] = tmp_arr[1] + 1
            # remove space
            for i in range(tmp_arr[0] - 1):
                self.__warehouse_left.pop(tmp_arr[1])
        else:
            self.__warehouse_right[tmp_arr[1]] = drawer
            tmp_arr[1] = tmp_arr[1] + 1
            # remove space
            for i in range(tmp_arr[0] - 1):
                self.__warehouse_right.pop(tmp_arr[1])

    # TODO: to finish
    def remove_drawer(self, drawer: Drawer):
        # check left column
        for i in range(len(self.__warehouse_left)):
            if self.__warehouse_left[i] is drawer:
                for j in range(Drawer.get_max_num_space(self.__warehouse_left[i])):
                    self.__warehouse_left.insert(i, 25)

                self.__warehouse_left.remove(drawer)

        # check right column
        for i in range(len(self.__warehouse_right)):
            if self.__warehouse_right[i] is drawer:
                for j in range(Drawer.get_max_num_space(self.__warehouse_right[i])):
                    self.__warehouse_right.insert(i, 25)

                self.__warehouse_right.remove(drawer)

    def __count_minimum_space(self, num_space: int, __warehouse: list):
        # set var
        min_space = self.__height
        count = 0
        start_index = 0

        for i in range(len(__warehouse) + 1):
            if i != len(__warehouse):
                # count number of space
                if __warehouse[i] == 25:
                    count = count + 1
                else:
                    # otherwise, if its minimum or it's the end of array
                    if (count < min_space) & (count >= num_space):
                        min_space = count
                        start_index = i - count

                    # restart the count with reset
                    count = 0
            else:
                if (count < min_space) & (count >= num_space):
                    min_space = count
                    start_index = i - count

                count = 0

        # if warehouse is empty
        if min_space == self.__height:
            # double check
            for i in range(len(__warehouse)):
                # if it isn't empty
                if isinstance(__warehouse[i], Drawer):
                    # raise IndexError("There isn't any space for this drawer.")
                    return -1
            min_space = len(__warehouse)

        # alloc only minimum space
        if min_space > num_space:
            min_space = num_space
        else:
            # otherwise there isn't any space
            if min_space < num_space:
                # raise IndexError("There isn't any space for this drawer.")
                return -1

        return [min_space, start_index]

    # TODO: debug
    def print_warehouse(self):
        print("LEFT: ")
        print(self.__warehouse_left)
        print("RIGHT: ")
        print(self.__warehouse_right)
