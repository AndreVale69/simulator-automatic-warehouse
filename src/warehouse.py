import copy
import simpy

from simpy import Environment
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Container.carousel import Carousel
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.drawer import Drawer


class Warehouse:
    def __init__(self):
        from src.useful_func import open_config

        config: dict = open_config()

        self.height = config["height_warehouse"]

        self.columns_container = []
        # add all columns taken from JSON
        for col_data in config["columns"]:
            self.add_column(Column(col_data))
        self.carousel = Carousel(config["carousel"])

        self.def_space = config["default_height_space"]
        self.speed_per_sec = config["speed_per_sec"]
        self.horiz_right_col = config["columns"][0]["horiz_distance"]
        self.horiz_left_col = config["columns"][1]["horiz_distance"]
        self.env = None
        self.floor = None

    def __deepcopy__(self, memo):
        copy_oby = Warehouse()
        copy_oby.height = self.height
        copy_oby.columns_container = copy.deepcopy(self.columns_container, memo)
        copy_oby.carousel = copy.deepcopy(self.carousel, memo)
        copy_oby.def_space = self.def_space
        copy_oby.speed_per_sec = self.speed_per_sec
        copy_oby.horiz_right_col = self.horiz_right_col
        copy_oby.horiz_left_col = self.horiz_left_col
        copy_oby.env = self.env
        copy_oby.floor = self.floor
        return copy_oby

    def get_height(self) -> int:
        return self.height

    def get_cols_container(self) -> list[Column]:
        return self.columns_container

    def get_carousel(self) -> Carousel:
        return self.carousel

    def get_environment(self) -> Environment:
        return self.env

    def get_floor(self):
        return self.floor

    def get_def_space(self) -> int:
        return self.def_space

    def get_speed_per_sec(self) -> int:
        return self.speed_per_sec

    def get_horiz_right_col(self) -> int:
        return self.horiz_right_col

    def get_horiz_left_col(self) -> int:
        return self.horiz_left_col

    def add_column(self, col: Column):
        self.get_cols_container().append(col)

    def check_buffer(self) -> bool:
        carousel = self.get_carousel().get_container()
        deposit = self.get_carousel().get_deposit()
        # check if the first position of buffer have a Drawer
        return True if type(carousel[deposit]) is DrawerEntry else False

    def check_deposit(self) -> bool:
        carousel = self.get_carousel().get_container()
        # check if the first position of deposit have a Drawer
        return True if type(carousel[0]) is DrawerEntry else False

    def come_back_to_deposit(self, drawer_inserted: Drawer):
        # take current position (y)
        curr_pos = drawer_inserted.get_first_drawerEntry().get_pos_x()

        # take destination position (y)
        dep_pos = DrawerEntry.get_pos_y(self.get_carousel().get_container()[0])

        yield self.env.timeout(self.vertical_move(curr_pos, dep_pos))

    def loading_buffer_and_remove(self, drawer_to_rmv: Drawer):
        storage = self.get_carousel().get_height_col()
        hole = self.get_carousel().get_hole()
        carousel = self.get_carousel().get_container()
        deposit = self.get_carousel().get_deposit()

        # calculate unload time
        pos_x_drawer = drawer_to_rmv.get_first_drawerEntry().get_pos_x()
        unload_time = self.__horiz_move(pos_x_drawer)

        # calculate loading buffer time
        start_pos = DrawerEntry.get_pos_y(carousel[deposit])
        end_pos = storage + hole
        loading_buffer_time = self.vertical_move(start_pos, end_pos)

        # choose greater time
        if unload_time > loading_buffer_time:
            yield self.env.timeout(unload_time)
        else:
            yield self.env.timeout(loading_buffer_time)

        # remove from container
        self.get_carousel().remove_drawer(drawer_to_rmv)

        # insert drawer in correct position (outside)
        drawer_to_show = DrawerEntry.get_drawer(carousel[deposit])
        self.get_carousel().add_drawer(True, drawer_to_show)

    def vertical_move(self, start_pos: int, end_pos: int) -> float:
        index_distance = abs(end_pos - start_pos)
        eff_distance = index_distance * self.get_def_space()
        vertical_move = (eff_distance / 100) / self.get_speed_per_sec()
        return vertical_move

    def allocate_best_pos(self, drawer: Drawer):
        from src.useful_func import check_minimum_space

        storage = self.get_carousel().get_height_col()
        hole = self.get_carousel().get_hole()

        start_pos = storage + hole
        minimum = check_minimum_space(self.get_cols_container(),
                                      drawer.get_max_num_space(),
                                      self.get_height() // self.get_def_space())
        pos_to_insert = minimum[1]

        # save temporarily the coordinates
        drawer.set_best_y(minimum[1])
        drawer.set_best_x(Column.get_pos_x(minimum[2]))

        vertical_move = self.vertical_move(start_pos, pos_to_insert)
        yield self.env.timeout(vertical_move)

    def unload(self, drawer: Drawer):
        pos_x_drawer = drawer.get_first_drawerEntry().get_pos_x()
        yield self.env.timeout(self.__horiz_move(pos_x_drawer))

    def load(self, drawer: Drawer):
        pos_x_drawer = drawer.get_best_x()
        pos_y_drawer = drawer.get_best_y()
        yield self.env.timeout(self.__horiz_move(pos_x_drawer))
        self.get_cols_container()[pos_x_drawer].    add_drawer(pos_y_drawer, drawer)

    def __horiz_move(self, pos_col: int):
        if pos_col == 0:
            return (self.get_horiz_right_col() / 100) / self.get_speed_per_sec()
        else:
            return (self.get_horiz_left_col() / 100) / self.get_speed_per_sec()

    def run_simulation(self, time: int, drawer: Drawer):
        from src.simulation import Floor

        self.env = simpy.Environment()
        self.floor = Floor(self.env, self)

        self.get_environment().process(self.get_floor().insert(drawer))
        self.get_environment().run(until=time)
