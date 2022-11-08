from src.useful_func import obt_value_json
from src.warehouse import Warehouse
from src.drawer import Drawer


class Floor(object):
    def __init__(self, env, warehouse: Warehouse, drawer: Drawer):
        self.env = env
        # start the move process everytime an instance is created.
        self.action = env.process(self.move(drawer))
        self.__warehouse = warehouse

    def move(self, drawer: Drawer):
        while True:
            print("Time %d - Start unload a drawer" % self.env.now)
            self.__unload()

            print("Time %d - Start vertical move" % self.env.now)

            self.__vertical_move()

    def __load(self):
        print("load")

    def __unload(self):
        horiz_move = (obt_value_json("horizontal_right_col") / 100) * obt_value_json("speed_per_sec")
        yield self.env.timeout(horiz_move)

    def __vertical_move(self, start_pos: int, end_pos: int):
        def_space = obt_value_json("default_height_space")
        index_distance = abs(end_pos - start_pos)
        eff_distance = index_distance * def_space
        vertical_move = (eff_distance / 100) * obt_value_json("speed_per_sec")
        yield self.env.timeout(vertical_move)
