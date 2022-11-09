from src.useful_func import obt_value_json, search_drawer, check_minimum_space
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.status_warehouse.Container.column import Column


class Floor(object):
    def __init__(self, env, warehouse: Warehouse, drawer: Drawer):
        self.env = env
        # start the move process everytime an instance is created.
        self.__warehouse = warehouse
        self.action = env.process(self.move(drawer))

    def move(self, drawer: Drawer):
        while True:
            print("Time %5d - Start unload a drawer" % self.env.now)
            yield self.env.process(self.__unload())
            drawer_entry = search_drawer(self.__warehouse.get_container(), drawer)
            minimum = check_minimum_space(self.__warehouse.get_container(),
                                          drawer.get_max_num_space())
            pos_to_insert = minimum[1]
            col = minimum[2]

            print("Time %5d - Start vertical move" % self.env.now)
            yield self.env.process(self.__vertical_move(drawer_entry.get_pos_y(), pos_to_insert))

            print("Time %5d - Start load a drawer" % self.env.now)
            yield self.env.process(self.__load(col, drawer, pos_to_insert))

            Column.remove_drawer(col, drawer)

    def __load(self, col_add: Column, drawer: Drawer, pos: int):
        horiz_move = (obt_value_json("horizontal_left_col") / 100) * obt_value_json("speed_per_sec")
        yield self.env.timeout(horiz_move)
        col_add.add_drawer(pos, drawer)

    def __unload(self):
        horiz_move = (obt_value_json("horizontal_right_col") / 100) * obt_value_json("speed_per_sec")
        yield self.env.timeout(horiz_move)

    def __vertical_move(self, start_pos: int, end_pos: int):
        def_space = obt_value_json("default_height_space")
        index_distance = abs(end_pos - start_pos)
        eff_distance = index_distance * def_space
        vertical_move = (eff_distance / 100) * obt_value_json("speed_per_sec")
        yield self.env.timeout(vertical_move)
