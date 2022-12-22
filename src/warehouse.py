import copy
import random
import simpy
from simpy import Environment

from src.status_warehouse.Container.column import Column
from src.status_warehouse.Container.carousel import Carousel
from src.status_warehouse.Entry.drawerEntry import DrawerEntry
from src.drawer import Drawer


class Warehouse:
    def __init__(self):
        from src.useful_func import open_config

        # open JSON configuration file
        config: dict = open_config()

        self.height = config["height_warehouse"]

        # add all columns taken from JSON
        self.columns_container = []
        for col_data in config["columns"]:
            self.add_column(Column(col_data))
        self.carousel = Carousel(config["carousel"])

        self.def_space = config["default_height_space"]
        self.speed_per_sec = config["speed_per_sec"]
        self.env = None
        self.floor = None
        self.supp_drawer = None

    def __deepcopy__(self, memo):
        copy_oby = Warehouse()
        copy_oby.height = self.get_height()
        copy_oby.columns_container = copy.deepcopy(self.get_cols_container(), memo)
        copy_oby.carousel = copy.deepcopy(self.get_carousel(), memo)
        copy_oby.def_space = self.get_def_space()
        copy_oby.speed_per_sec = self.get_speed_per_sec()
        copy_oby.env = self.get_environment()
        copy_oby.floor = self.get_floor()
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

    def get_drawer_of_support(self) -> Drawer:
        return self.supp_drawer

    def add_column(self, col: Column):
        self.get_cols_container().append(col)

    def set_drawer_of_support(self, drawer: Drawer):
        self.supp_drawer = drawer

    def check_buffer(self) -> bool:
        """
        Check the buffer
        :return: True if is full, False otherwise
        """
        carousel = self.get_carousel().get_container()
        deposit = self.get_carousel().get_deposit()
        # TODO: get_deposit_container -> Carousel
        # check if the first position of buffer have a Drawer
        return True if type(carousel[deposit]) is DrawerEntry else False

    def check_deposit(self) -> bool:
        """
        Check the deposit
        :return: True if is full, False otherwise
        """
        carousel = self.get_carousel().get_container()
        # check if the first position of deposit have a Drawer
        return True if type(carousel[0]) is DrawerEntry else False

    def come_back_to_deposit(self, drawer_inserted: Drawer):
        # take current position (y)
        curr_pos = drawer_inserted.get_first_drawerEntry().get_pos_y()

        # take destination position (y)
        dep_pos = DrawerEntry.get_pos_y(self.get_carousel().get_container()[0])

        yield self.env.timeout(self.vertical_move(curr_pos, dep_pos))

    def loading_buffer_and_remove(self):
        storage: int = self.get_carousel().get_height_col()
        hole: int = self.get_carousel().get_hole()
        carousel: list = self.get_carousel().get_container()
        deposit: int = self.get_carousel().get_deposit()

        # calculate loading buffer time
        start_pos = carousel[deposit].get_pos_y()
        end_pos = storage + hole
        loading_buffer_time = self.vertical_move(start_pos, end_pos)

        yield self.env.timeout(loading_buffer_time)

        # obtain the drawer inside the buffer
        drawer_to_show = carousel[deposit].get_drawer()
        # remove from buffer
        self.get_carousel().remove_drawer(drawer_to_show)
        # and insert drawer in correct position (outside)
        self.get_carousel().add_drawer(True, drawer_to_show)

        print(f"Time {self.env.now:5.2f} - Finish loading buffer drawer inside the deposit")

    def vertical_move(self, start_pos: int, end_pos: int) -> float:
        # calculate the distance of index between two points
        index_distance = abs(end_pos - start_pos)
        # calculate effective distance with real measures
        eff_distance = index_distance * self.get_def_space()
        # formula of vertical move
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
        drawer.set_best_offset_x(Column.get_offset_x(minimum[2]))

        vertical_move = self.vertical_move(start_pos, pos_to_insert)
        yield self.env.timeout(vertical_move)

    def unload(self, drawer: Drawer):
        offset_x_drawer = drawer.get_first_drawerEntry().get_offset_x()
        yield self.env.timeout(self.horiz_move(offset_x_drawer))

    def load(self, drawer: Drawer):
        pos_x_drawer = drawer.get_best_offset_x()
        pos_y_drawer = drawer.get_best_y()
        yield self.env.timeout(self.horiz_move(pos_x_drawer))
        index = self.__minimum_offset(self.get_cols_container())
        self.get_cols_container()[index].add_drawer(pos_y_drawer, drawer)

    def horiz_move(self, offset_x: int):
        """
        Search in the column/carousel where is the drawer
        :param offset_x: offset of the drawer to search
        :return: the time estimated
        """
        # check the carousel
        if self.get_carousel().get_offset_x() == offset_x:
            return (self.get_carousel().get_width() / 100) / self.get_speed_per_sec()
        else:
            # check every column
            for elem in self.get_cols_container():
                if elem.get_offset_x() == offset_x:
                    return (elem.get_width() / 100) / self.get_speed_per_sec()

    def __minimum_offset(self, container) -> int:
        """
        Calculate the minimum offset between the columns
        :param container: list of columns or carousels
        :return: the index of the list
        """
        min_offset = container[0].get_offset_x()
        index = 0
        for i, column in enumerate(self.get_cols_container()):
            if min_offset < column.get_offset_x():
                min_offset = column.get_offset_x()
                index = i
        return index

    # TODO: gen_rand della popolazione del warehouse in base ai parametri (quanti cassetti, quanti materiali)

    # TODO: in Material
    def gen_rand_material(self):
        from src.material import Material

        name_materials = ['Shirt',
                          'Pasta',
                          'Tomato',
                          'Bottle',
                          'Tablet',
                          'Helmet']

        # multiply for current time to avoid the same barcode
        barcode = random.randint(100_000_000, 999_999_999) * self.env.now
        name = random.choice(name_materials)
        # height max is buffer height = 150
        height = random.randint(25, 150)
        length = random.randint(25, 150)
        width = random.randint(25, 150)

        return Material(barcode, name, height, length, width)

    # TODO: get_rand_materials in base al parametro crea materiali chiamando gen_rand_material()

    def run_simulation(self, time: int):
        from src.simulation import Simulation

        self.env = simpy.Environment()
        self.floor = Simulation(self.env, self)

        self.get_environment().process(self.get_floor().simulate_actions(self.floor.insert_material_and_alloc_drawer))

        self.get_environment().run(until=time)
