import copy
import random

import simpy
from simpy import Environment

from src.drawer import Drawer
from src.status_warehouse.Container.carousel import Carousel
from src.status_warehouse.Container.column import Column
from src.status_warehouse.Entry.drawerEntry import DrawerEntry


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
        file.write(f"Number of spaces    : {self.get_carousel().get_num_entries_free()}\n")
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
            file.write(f"Number of spaces    : {column.get_num_entries_free()}\n")
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


def gen_materials_and_drawer(num_drawers: int, num_materials: int,
                             rand_num_drawers: int, col: Column) -> list:
    """
    Generate drawers and materials
    :param num_drawers: number of drawers to create in the warehouse
    :param num_materials: number of materials to create in the drawers
    :param rand_num_drawers: number of drawers to generate
    :param col: column selected where to put the drawers
    :return: [number of drawers left, number of materials left]
    """
    from src.material import gen_rand_materials

    # generate "rand_num_drawers" drawers
    for rand_num in range(rand_num_drawers):
        num_materials_to_put = 0
        materials = None
        # check if there are materials to generate
        if num_materials > 0:
            # generate a value of materials to insert
            num_materials_to_put = random.randint(1, num_materials)
            materials = gen_rand_materials(num_materials_to_put)

        # check if there is space in warehouse
        remaining_avail_entry = col.get_height_col() - col.get_num_entries_occupied()
        if remaining_avail_entry >= 1:
            # insert empty drawer
            drawer_to_insert = Drawer(materials)
            # looking for the index where put the drawer
            index = check_minimum_space([col], drawer_to_insert.get_max_num_space(), col.get_height_col())[1]
            # if the height is correct, insert
            if index != -1:
                # insert the drawer
                col.add_drawer(drawer_to_insert, index)
                # update local counter
                num_materials -= num_materials_to_put
                num_drawers -= 1
        # if there isn't space in the column
        else:
            # stop to put drawers inside this column
            break

    return [num_drawers, num_materials]


def check_minimum_space(list_obj: list, space_req: int, height_entry_col: int) -> list:
    """
    Algorithm to decide where insert a drawer.

    :param list_obj: list of columns.
    :param space_req: space requested from drawer.
    :param height_entry_col: the height of warehouse
    :return: if there is a space [space_requested, index_position_where_insert, column_where_insert].
    :exception StopIteration: if there isn't any space.
    """
    result = []
    col = None

    # calculate minimum space and search lower index
    for column in list_obj:
        [min_space, start_index] = min_search_alg(column, space_req)
        if min_space != -1 and start_index < height_entry_col:
            result = [min_space, start_index]
            col = column

    # if warehouse is full
    if col is None:
        return [-1, -1, -1]
    else:
        result.append(col)
        return result


def min_search_alg(self, space_req: int) -> list:
    """
    Algorithm to calculate a minimum space inside a column.

    :param self: object to calculate minimum space.
    :param space_req: space requested from drawer.
    :return: negative values if there isn't any space, otherwise [space_requested, index_position_where_insert].
    """
    from src.status_warehouse.Entry.emptyEntry import EmptyEntry
    min_space = self.get_height_warehouse()
    count = 0
    start_index = self.get_height_last_position() - 1
    container = self.get_container()
    height_last_pos = self.get_height_last_position()
    index = height_last_pos

    ############################
    # Minimum search algorithm #
    ############################

    # verify the highest position
    if type(container[start_index]) is EmptyEntry and space_req <= height_last_pos:
        min_space = height_last_pos
        return [min_space, start_index]

    for i in range(index, len(container)):
        entry = container[i]
        index += 1
        # if the position is empty
        if type(entry) is EmptyEntry:
            # count number of spaces
            count += 1
        else:
            # otherwise, if it's minimum and there is enough space
            if (count < min_space) & (count >= space_req):
                # update check values
                min_space = count
                start_index = index - count
            # restart the count with reset
            count = 0

    # if warehouse is empty
    if min_space == self.get_height_warehouse():
        if count == 0:
            # double security check
            for entry in container:
                # if it isn't empty
                if type(entry) is Drawer:
                    # raise IndexError("There isn't any space for this drawer.")
                    return [-1, -1]
            min_space = len(container)
        else:
            # update check values
            min_space = count
            start_index = index - count

    # if the last position is better and free
    if space_req < height_last_pos < min_space and type(container[height_last_pos - 1]) is EmptyEntry:
        min_space = space_req
        start_index = height_last_pos - 1
    else:
        # alloc only minimum space
        if min_space >= space_req:
            min_space = space_req
        else:
            # otherwise there isn't any space
            if min_space < space_req:
                # raise IndexError("There isn't any space for this drawer.")
                return [-1, -1]

    return [min_space, start_index]


class Warehouse:
    def __init__(self):
        from src.useful_func import open_config

        # open JSON configuration file
        config: dict = open_config()

        self.height = config["height_warehouse"]

        # add all columns taken from JSON
        self.columns_container = []
        # all columns must be added from minimum offset_x to greats offset_x
        # respecting this order
        for col_data in config["columns"]:
            self.add_column(Column(col_data, self))
        self.carousel = Carousel(config["carousel"], self)

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

    def get_max_height_material(self) -> int:
        return self.max_height_material

    def add_column(self, col: Column):
        self.get_cols_container().append(col)

    def minimum_offset(self, container) -> int:
        """
        Calculate the minimum offset between the columns
        :param container: list of columns or carousels
        :return: the index of the list
        """
        min_offset = container[0].get_offset_x()
        index = 0
        for i, column in enumerate(self.get_cols_container()):
            if column.get_offset_x() < min_offset:
                min_offset = column.get_offset_x()
                index = i
        return index

    def is_full(self) -> bool:
        """Verify if there is a space inside the warehouse"""
        for col in self.get_cols_container():
            if col.get_num_entries_free() > 0:
                return False
        return True

    def come_back_to_deposit(self, drawer_inserted: Drawer):
        # take current position (y)
        curr_pos = drawer_inserted.get_first_drawerEntry().get_pos_y()
        # take destination position (y)
        dep_pos = self.get_carousel().get_deposit_entry().get_pos_y()
        yield self.env.timeout(self.vertical_move(curr_pos, dep_pos))

    def go_to_buffer(self, drawer_inserted: Drawer):
        # take current position (y)
        curr_pos = drawer_inserted.get_first_drawerEntry().get_pos_y()
        # take destination position (y)
        buf_pos = self.get_carousel().get_buffer_entry().get_pos_y()
        yield self.env.timeout(self.vertical_move(curr_pos, buf_pos))

    def load_in_carousel(self, drawer_to_insert: Drawer, destination, load_in_buffer: bool):
        y_dep = self.get_carousel().get_deposit_entry().get_pos_y()
        y_buf = self.get_carousel().get_buffer_entry().get_pos_y()
        # update the y position
        drawer_to_insert.set_best_y(y_dep)

        # calculate time to move (y)
        if load_in_buffer:
            # if the deposit is full but the buffer isn't full
            if not self.get_carousel().is_buffer_full():
                # update the y destination
                drawer_to_insert.set_best_y(y_buf)
                print(f"Time {self.env.now:5.2f} - Deposit is full! Start vertical move to buffer")
                yield self.env.timeout(self.vertical_move(start_pos=y_dep, end_pos=y_buf))
                print(f"Time {self.env.now:5.2f} - Start to load in the buffer")
            else:
                raise NotImplementedError("Deposit and buffer are full! Collision!")

        # and load inside the carousel
        yield self.env.process(self.load(drawer_to_insert, destination))

    def loading_buffer_and_remove(self):
        buffer: DrawerEntry = self.get_carousel().get_buffer_entry()

        # calculate loading buffer time
        start_pos = buffer.get_pos_y()
        end_pos = self.get_carousel().get_deposit_entry().get_pos_y()
        loading_buffer_time = self.vertical_move(start_pos, end_pos)

        yield self.env.timeout(loading_buffer_time)

        # obtain the drawer inside the buffer
        drawer_to_show = buffer.get_drawer()
        # remove from buffer
        self.get_carousel().remove_drawer(drawer_to_show)
        # and insert drawer in correct position (outside)
        self.get_carousel().add_drawer(drawer_to_show)

    def vertical_move(self, start_pos: int, end_pos: int) -> float:
        # calculate the distance of index between two points
        index_distance = abs(end_pos - start_pos)
        # calculate effective distance with real measures
        eff_distance = index_distance * self.get_def_space()
        # formula of vertical move
        vertical_move = (eff_distance / 100) / self.get_speed_per_sec()
        return vertical_move

    def allocate_best_pos(self, drawer: Drawer):
        # start position
        start_pos = self.get_carousel().get_deposit_entry().get_pos_y()
        # calculate destination position
        minimum = check_minimum_space(self.get_cols_container(),
                                      drawer.get_max_num_space(),
                                      self.get_height() // self.get_def_space())
        pos_to_insert = minimum[1]
        # save temporarily the coordinates
        drawer.set_best_y(minimum[1])
        drawer.set_best_offset_x(Column.get_offset_x(minimum[2]))
        # start the move
        vertical_move = self.vertical_move(start_pos, pos_to_insert)
        yield self.env.timeout(vertical_move)

    def reach_drawer_height(self, drawer: Drawer):
        # save coordinates inside drawer
        drawer.set_best_y(drawer.get_first_drawerEntry().get_pos_y())
        drawer.set_best_offset_x(drawer.get_first_drawerEntry().get_offset_x())
        # start the move
        vertical_move = self.vertical_move(start_pos=self.get_carousel().get_deposit_entry().get_pos_y(),
                                           end_pos=drawer.get_first_drawerEntry().get_pos_y())
        yield self.env.timeout(vertical_move)

    def unload(self, drawer: Drawer):
        # take x offset
        offset_x_drawer = drawer.get_first_drawerEntry().get_offset_x()
        # start the move
        yield self.env.timeout(self.horiz_move(offset_x_drawer))
        # update warehouse
        # if drawer hasn't been removed
        if not self.get_carousel().remove_drawer(drawer):
            # find in a column and terminate
            for col in self.get_cols_container():
                if col.remove_drawer(drawer):
                    break

    def load(self, drawer: Drawer, destination: str):
        from src.status_warehouse.enum_warehouse import EnumWarehouse
        # take destination coordinates
        dest_x_drawer = drawer.get_best_offset_x()
        dest_y_drawer = drawer.get_best_y()
        # start the move
        yield self.env.timeout(self.horiz_move(dest_x_drawer))
        # update warehouse
        # if destination is carousel, add
        if destination == EnumWarehouse.CAROUSEL:
            self.get_carousel().add_drawer(drawer, dest_y_drawer)
        else:
            # otherwise, check the offset of column
            for col in self.get_cols_container():
                if col.get_offset_x() == dest_x_drawer:
                    col.add_drawer(drawer, dest_y_drawer)
                    break

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
            for col in self.get_cols_container():
                if col.get_offset_x() == offset_x:
                    return (col.get_width() / 100) / self.get_speed_per_sec()

    def gen_rand(self, num_drawers: int, num_materials: int):
        """Generate a random warehouse"""
        warehouse_is_full = False

        # until there are drawers to insert and the warehouse isn't full
        while num_drawers > 0 and not warehouse_is_full:
            # check available space in warehouse
            if self.is_full():
                warehouse_is_full = True
            else:
                # choice a random column
                rand_col: Column = random.choice(self.get_cols_container())
                # generate random number to decide how many drawers insert inside the column
                rand_num_drawers = random.randint(1, num_drawers)
                [num_drawers, num_materials] = gen_materials_and_drawer(num_drawers, num_materials,
                                                                        rand_num_drawers, rand_col)
        # if there aren't anything else to add
        if num_drawers == 0 and num_materials == 0:
            print("The creation of random warehouse is completed.")
        else:
            # if there aren't more drawers but some materials...
            if num_drawers == 0:
                print(f"num_materials left: {num_materials}")
            else:
                # if the warehouse is completely full
                print(f"The warehouse is full, num_drawers left: {num_drawers}, num_materials left: {num_materials}")

    def run_simulation(self, time: int, num_actions: int):
        from src.simulation import Simulation

        self.env = simpy.Environment()
        self.simulation = Simulation(self.env, self)

        balance_wh = 0
        # create list of event alias
        alias_events = ["send_back", "extract_drawer", "ins_mat", "rmv_mat"]
        events_to_simulate = []

        # if the deposit or the buffer are full, then update the counter
        if type(self.get_carousel().get_deposit_entry()) is DrawerEntry:
            balance_wh += 1
        if type(self.get_carousel().get_buffer_entry()) is DrawerEntry:
            balance_wh += 1

        for num_action in range(num_actions):
            good_choice = False
            rand_event = ""
            while good_choice is False:
                # select an event
                rand_event = random.choice(alias_events)
                # check the if the choice is correct
                if 1 <= balance_wh <= 2 and (rand_event == "send_back" or
                                             rand_event == "ins_mat" or
                                             rand_event == "rmv_mat"):
                    good_choice = True
                    if rand_event == "send_back":
                        balance_wh -= 1
                else:
                    if 0 <= balance_wh < 2 and rand_event == "extract_drawer":
                        good_choice = True
                        balance_wh += 1
            events_to_simulate.append(rand_event)

        # create the simulation
        self.get_environment().process(self.get_simulation().simulate_actions(events_to_simulate))

        # run simulation
        self.get_environment().run(until=time)

    def choice_random_drawer(self) -> Drawer:
        """Choose a random drawer from the warehouse"""
        container_drawer_entry = []
        for col in self.get_cols_container():
            # if there aren't any drawer
            if col.get_num_entries_occupied() == 0:
                continue
            else:
                # otherwise, build the list
                container_drawer_entry.extend(col.get_drawers())
        if len(container_drawer_entry) == 0:
            print("The warehouse is empty!")
        else:
            return random.choice(container_drawer_entry)
