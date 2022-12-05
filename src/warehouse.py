import copy
import simpy

from simpy import Environment
from src.useful_func import obt_value_json, search_drawer, check_minimum_space
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Container.carousel import Carousel
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.drawer import Drawer


class Warehouse:
    def __init__(self):
        self.height = obt_value_json("height_warehouse")
        self.container = []
        self.carousel = Carousel(0)
        self.def_space = obt_value_json("default_height_space")
        self.speed_per_sec = obt_value_json("speed_per_sec")
        self.horiz_left_col = obt_value_json("horiz_distance", "sxcol")
        self.horiz_right_col = obt_value_json("horiz_distance", "rxcol")
        self.env = None
        self.floor = None

    def __deepcopy__(self, memo):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        self.carousel = copy.deepcopy(self.carousel, memo)
        self.container = copy.deepcopy(self.container, memo)
        return newone

    def get_height(self) -> int:
        return self.height

    def get_container(self) -> list[Column]:
        return self.container

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

    def add_container(self, container: Column):
        self.get_container().append(container)

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
        try:
            curr_pos = search_drawer(self.get_container(), drawer_inserted).get_pos_x()
        except StopIteration:
            curr_pos = search_drawer([self.get_carousel()], drawer_inserted).get_pos_x()

        # take destination position (y)
        dep_pos = DrawerEntry.get_pos_y(self.get_carousel().get_container()[0])

        yield self.env.timeout(self.vertical_move(curr_pos, dep_pos))

    def loading_buffer_and_remove(self, drawer_to_rmv: Drawer):
        storage = self.get_carousel().get_storage()
        hole = self.get_carousel().get_hole()
        carousel = self.get_carousel().get_container()
        deposit = self.get_carousel().get_deposit()

        # calculate unload time
        try:
            pos_x_drawer = search_drawer(self.get_container(), drawer_to_rmv).get_pos_x()
        except StopIteration:
            pos_x_drawer = search_drawer([self.get_carousel()], drawer_to_rmv).get_pos_x()
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
        storage = self.get_carousel().get_storage()
        hole = self.get_carousel().get_hole()

        start_pos = storage + hole
        minimum = check_minimum_space(self.get_container(), drawer.get_max_num_space())
        pos_to_insert = minimum[1]

        # save temporarily the coordinates
        drawer.set_best_y(minimum[1])
        drawer.set_best_x(Column.get_pos_x(minimum[2]))

        vertical_move = self.vertical_move(start_pos, pos_to_insert)
        yield self.env.timeout(vertical_move)

    def unload(self, drawer: Drawer):
        try:
            pos_x_drawer = search_drawer(self.get_container(), drawer).get_pos_x()
        except StopIteration:
            pos_x_drawer = search_drawer([self.get_carousel()], drawer).get_pos_x()
        yield self.env.timeout(self.__horiz_move(pos_x_drawer))

    def load(self, drawer: Drawer):
        pos_x_drawer = drawer.get_best_x()
        pos_y_drawer = drawer.get_best_y()
        yield self.env.timeout(self.__horiz_move(pos_x_drawer))
        self.get_container()[pos_x_drawer].add_drawer(pos_y_drawer, drawer)

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
