from src.drawer import Drawer


class Warehouse(object):
    # __type = np.dtype([("name", "U30"), ("drawer", Drawer)])
    # __warehouse = np.array([], dtype=__type)
    __warehouse = []
    __height = 0
    __minimum_height = 500

    def __init__(self, height: int):
        self.__height = height

        # error
        if height < self.__minimum_height:
            raise ValueError("The height is too low, please digit a value grater/equal than " +
                             str(self.__minimum_height))

        # creation of space
        num_space = height // 25
        for i in range(num_space):
            self.__warehouse.append(25)

    def set_height(self, height: int):
        self.__height = height

    def get_height(self):
        return self.__height

    def get_warehouse(self):
        return self.__warehouse

    def add_drawer(self, drawer: Drawer):
        tmp_arr = self.__count_minimum_space(drawer.get_max_num_space())
        # Help
        #   tmp_arr:
        #           temp_arr[0] = min_space   --> numbers of elements to remove
        #           temp_arr[1] = start_index --> start index on __warehouse list

        # insert element
        self.__warehouse[tmp_arr[1]] = drawer
        tmp_arr[1] = tmp_arr[1] + 1

        # remove space
        for i in range(tmp_arr[0] - 1):
            self.__warehouse.pop(tmp_arr[1])

    # TODO: to finish
    def remove_drawer(self, drawer: Drawer):
        for i in range(len(self.__warehouse)):
            if self.__warehouse[i] is drawer:
                for j in range(Drawer.get_max_num_space(self.__warehouse[i])):
                    self.__warehouse.insert(i, 25)

                self.__warehouse.remove(drawer)

    def __count_minimum_space(self, num_space: int):
        # set var
        min_space = self.__height
        count = 0
        start_index = 0

        for i in range(len(self.__warehouse) + 1):
            if i != len(self.__warehouse):
                # count number of space
                if self.__warehouse[i] == 25:
                    count = count + 1
                else:
                    #print("Count: " + str(count))
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
            for i in range(len(self.__warehouse)):
                # if it isn't empty
                if isinstance(self.__warehouse[i], Drawer):
                    raise IndexError("There isn't any space for this drawer.")

            min_space = len(self.__warehouse)

        # alloc only minimum space
        if min_space > num_space:
            min_space = num_space
        else:
            # otherwise there isn't any space
            if min_space < num_space:
                raise IndexError("There isn't any space for this drawer.")

        return [min_space, start_index]

    # TODO: debug
    def print_warehouse(self):
        print(self.__warehouse)
