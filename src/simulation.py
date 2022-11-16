import copy
from src.useful_func import obt_value_json, search_drawer, check_minimum_space
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.status_warehouse.Container.column import Column


class Floor(object):
    def __init__(self, env, warehouse: Warehouse, drawer: Drawer):
        self.env = env
        # start the move process everytime an instance is created.
        self.__warehouse = copy.copy(warehouse)
        self.__horiz_left_col = obt_value_json("horizontal_left_col")
        self.__horiz_right_col = obt_value_json("horizontal_right_col")
        self.__def_space = obt_value_json("default_height_space")
        self.__speed_per_sec = obt_value_json("speed_per_sec")
        self.action = env.process(self.move(drawer))

    def move(self, drawer: Drawer):
        while True:
            print(f"Time {self.env.now:5.2f} - Start unload a drawer")
            yield self.env.process(self.__unload())
            drawer_entry = search_drawer(self.__warehouse.get_container(), drawer)
            minimum = check_minimum_space(self.__warehouse.get_container(),
                                          drawer.get_max_num_space())
            pos_to_insert = minimum[1]
            col = minimum[2]

            print(f"Time {self.env.now:5.2f} - Start vertical move")
            yield self.env.process(self.__vertical_move(drawer_entry.get_pos_y(), pos_to_insert))

            print(f"Time {self.env.now:5.2f} - Start load a drawer")
            yield self.env.process(self.__load(col, drawer, pos_to_insert))

            col.remove_drawer(drawer)

    def get_warehouse(self) -> Warehouse:
        return self.__warehouse

    def get_horiz_left_col(self) -> int:
        return self.__horiz_left_col

    def get_horiz_right_col(self) -> int:
        return self.__horiz_right_col

    def get_def_space(self) -> int:
        return self.__def_space

    def get_speed_per_sec(self) -> int:
        return self.__speed_per_sec

    def __load(self, col_add: Column, drawer: Drawer, pos: int):
        # TODO check m * m/s -> m^2/s
        horiz_move = (self.get_horiz_left_col() / 100) / self.get_speed_per_sec()
        yield self.env.timeout(horiz_move)
        col_add.add_drawer(pos, drawer)

    def __unload(self):
        horiz_move = (self.get_horiz_right_col() / 100) / self.get_speed_per_sec()
        yield self.env.timeout(horiz_move)

    def __vertical_move(self, start_pos: int, end_pos: int):
        index_distance = abs(end_pos - start_pos)
        eff_distance = index_distance * self.get_def_space()
        vertical_move = (eff_distance / 100) * self.get_speed_per_sec()
        yield self.env.timeout(vertical_move)
