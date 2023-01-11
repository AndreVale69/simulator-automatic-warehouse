import copy
import random

import simpy
from simpy import Environment

from src.drawer import Drawer
from src.status_warehouse.Container.carousel import Carousel
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


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
        self.max_height_material = config["carousel"]["buffer_height"] // self.get_def_space()
        self.env = None
        self.simulation = None
        self.supp_drawer = None

    def __deepcopy__(self, memo):
        copy_oby = Warehouse()
        copy_oby.height = self.get_height()
        copy_oby.columns_container = copy.deepcopy(self.get_cols_container(), memo)
        copy_oby.carousel = copy.deepcopy(self.get_carousel(), memo)
        copy_oby.def_space = self.get_def_space()
        copy_oby.speed_per_sec = self.get_speed_per_sec()
        copy_oby.env = self.get_environment()
        copy_oby.simulation = self.get_simulation()
        return copy_oby

    def get_height(self) -> int:
        return self.height

    def get_cols_container(self) -> list[Column]:
        return self.columns_container

    def get_carousel(self) -> Carousel:
        return self.carousel

    def get_environment(self) -> Environment:
        return self.env

    def get_simulation(self):
        return self.simulation

    def get_def_space(self) -> int:
        return self.def_space

    def get_speed_per_sec(self) -> int:
        return self.speed_per_sec

    def get_drawer_of_support(self) -> Drawer:
        return self.supp_drawer

    def get_max_height_material(self) -> int:
        return self.max_height_material

    def add_column(self, col: Column):
        self.get_cols_container().append(col)

    def set_drawer_of_support(self, drawer: Drawer):
        self.supp_drawer = drawer

    def check_buffer(self) -> bool:
        """
        Check the buffer
        :return: True if is full, False otherwise
        """
        # check if the first position of buffer have a Drawer
        return True if type(self.get_carousel().get_buffer_entry()) is DrawerEntry else False

    def check_deposit(self) -> bool:
        """
        Check the deposit
        :return: True if is full, False otherwise
        """
        # check if the first position of deposit have a Drawer
        return True if type(self.get_carousel().get_deposit_entry()) is DrawerEntry else False

    def come_back_to_deposit(self, drawer_inserted: Drawer):
        # take current position (y)
        curr_pos = drawer_inserted.get_first_drawerEntry().get_pos_y()

        # take destination position (y)
        dep_pos = DrawerEntry.get_pos_y(self.get_carousel().get_deposit_entry())

        yield self.env.timeout(self.vertical_move(curr_pos, dep_pos))

    def loading_buffer_and_remove(self):
        storage: int = self.get_carousel().get_height_col()
        hole: int = self.get_carousel().get_hole()
        buffer: DrawerEntry = self.get_carousel().get_buffer_entry()

        # calculate loading buffer time
        start_pos = buffer.get_pos_y()
        end_pos = storage + hole
        loading_buffer_time = self.vertical_move(start_pos, end_pos)

        yield self.env.timeout(loading_buffer_time)

        # obtain the drawer inside the buffer
        drawer_to_show = buffer.get_drawer()
        # remove from buffer
        self.get_carousel().remove_drawer(drawer_to_show)
        # and insert drawer in correct position (outside)
        self.get_carousel().add_drawer(drawer_to_show)

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
        index = self.minimum_offset(self.get_cols_container())
        self.get_cols_container()[index].add_drawer(drawer, pos_y_drawer)

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

    def minimum_offset(self, container) -> int:
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

    def gen_rand(self, num_drawers: int, num_materials: int):
        """Generate a random warehouse"""
        num_cols_full = 0

        if num_drawers > num_materials:
            raise ValueError("Materials must be greater than Drawers.")

        # start to populate every column
        for col in self.get_cols_container():
            if num_drawers > 0:
                # generate random number to decide how many drawers insert inside the column
                rand_num_drawers = random.randint(1, num_drawers)
                [num_drawers, num_materials, num_cols_full] = self.gen_materials_and_drawer(num_drawers, num_materials,
                                                                                            rand_num_drawers, col)
            else:
                # if there aren't more drawers
                break

        # if there aren't anything else to add
        if num_drawers == 0 and num_materials == 0:
            print("The creation of random warehouse is completed.")
        else:
            # if there aren't more drawers but some materials...
            if num_drawers == 0:
                print(f"num_materials left: {num_materials}")
            else:
                # if the warehouse is completely full, terminate
                if num_cols_full == len(self.get_cols_container()):
                    print(
                        f"The warehouse is full, num_drawers left: {num_drawers}, num_materials left: {num_materials}")
                else:
                    # otherwise, recursive call
                    self.gen_rand(num_drawers, num_materials)

    def gen_materials_and_drawer(self, num_drawers: int, num_materials: int, rand_num_drawers: int, col: Column) -> list:
        """Generate drawers and materials"""
        from src.material import gen_rand_materials

        num_cols_full = 0

        for i in range(rand_num_drawers):
            # if there are more materials than drawers, that is if there are surplus of materials
            if (num_materials - num_drawers) > 1:
                # how many materials insert inside the drawer
                num_materials_to_put = random.randint(1, num_materials - num_drawers)
            else:
                num_materials_to_put = 1
            # check the height remaining
            remaining_avail_entry = col.get_height_col() - col.get_entry_occupied()
            # and generate material(s)
            if remaining_avail_entry >= self.get_max_height_material():
                materials = gen_rand_materials(num_materials_to_put)
            else:
                # if the remaining available entry is less than 1
                if remaining_avail_entry < 1:
                    # stop to put drawers inside this column
                    num_cols_full += 1
                    break
                else:
                    # insert materials with specific height
                    materials = gen_rand_materials(num_materials_to_put,
                                                   max_limit=remaining_avail_entry * self.get_def_space())

            # update local counter
            num_materials -= num_materials_to_put
            # generate the drawer
            self.gen_drawer(materials, col)
            # update local counter
            num_drawers -= 1

        return [num_drawers, num_materials, num_cols_full]

    def gen_drawer(self, materials: list, col: Column):
        """Generate a Drawer"""
        from src.useful_func import check_minimum_space

        # insert the material(s) inside drawer
        drawer_to_insert = Drawer(materials)
        # looking for the index where put the drawer
        index = check_minimum_space([col], drawer_to_insert.get_max_num_space(), col.get_height_col())[1]
        # insert the drawer
        col.add_drawer(drawer_to_insert, index)

    def run_simulation(self, time: int):
        from src.simulation import Simulation

        self.env = simpy.Environment()
        self.simulation = Simulation(self.env, self)

        self.get_environment().process(self.get_simulation().
                                       simulate_actions(self.get_simulation().insert_material_and_alloc_drawer))

        self.get_environment().run(until=time)

    def save_config(self):
        # opening JSON file
        with open("../tmp/config_warehouse.txt", 'w') as file:
            # header
            file.write(f"Warehouse situation\n")
            file.write("\n")
            file.write("~" * 40 + "\n")
            file.write("\n")

            # carousel
            file.write(f"Number of drawers   : {self.get_carousel().get_num_drawers()}\n")
            file.write(f"Number of spaces    : {self.get_carousel().get_num_spaces()}\n")
            file.write(f"Number of materials : {self.get_carousel().get_num_materials()}\n")
            file.write("Carousel:\n")
            for entry in self.get_carousel().get_container():
                if type(entry) is DrawerEntry:
                    file.write(f"[{entry}, {entry.get_drawer()}]\n")
                else:
                    file.write(f"[{entry}]\n")
            file.write("\n")
            file.write("~" * 40 + "\n")
            file.write("\n")

            # columns
            for column in self.get_cols_container():
                file.write(f"Number of drawers   : {column.get_num_drawers()}\n")
                file.write(f"Number of spaces    : {column.get_num_spaces()}\n")
                file.write(f"Number of materials : {column.get_num_materials()}\n")
                file.write(f"Column[{column.get_offset_x()}]\n")
                for entry in column.get_container():
                    if type(entry) is DrawerEntry:
                        file.write(f"[{entry}, {entry.get_drawer()}]\n")
                    else:
                        file.write(f"[{entry}]\n")
                file.write("\n")
                file.write("~" * 40 + "\n")
                file.write("\n")

        # import subprocess
        # path_to_notepad = "C:\\Windows\\System32\\notepad.exe"
        # path_to_file = "../tmp/config_warehouse.txt"
        # subprocess.call([path_to_notepad, path_to_file])
