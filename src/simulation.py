import copy

from simpy import Environment
from src.warehouse import Warehouse
from src.drawer import Drawer


class Floor(object):
    def __init__(self, env: Environment, warehouse: Warehouse):
        self.env = env
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)
        # self.action = env.process(self.move(drawer))

    def get_warehouse(self) -> Warehouse:
        return self.warehouse

    def insert(self, drawer: Drawer):
        print(f"Time {self.env.now:5.2f} - Start unloading a drawer")

        # check if the buffer is to load or not
        if self.get_warehouse().check_buffer():
            print(f"Time {self.env.now:5.2f} - Start loading buffer drawer inside the deposit")
            yield self.env.process(self.get_warehouse().loading_buffer_and_remove(drawer))
        else:
            # unloading drawer
            yield self.env.process(self.get_warehouse().unload(drawer))
            # remove only from container
            self.get_warehouse().get_carousel().remove_drawer(drawer)

        # move the floor
        print(f"Time {self.env.now:5.2f} - Start vertical move")
        yield self.env.process(self.get_warehouse().allocate_best_pos(drawer))

        # add the drawer
        print(f"Time {self.env.now:5.2f} - Start loading a drawer")
        yield self.env.process(self.get_warehouse().load(drawer))

        print(f"Time {self.env.now:5.2f} - Finish")
        # TODO: return to deposit

    def remove(self):
        print("Remove")

    def search_material(self):
        print("Search")
        print("Insert or Remove")

    def move(self, drawer: Drawer):
        while True:
            print("To rmv")
            # drawer_entry = search_drawer(self.__warehouse.get_container(), drawer)
            # minimum = check_minimum_space(self.__warehouse.get_container(),
            #                               drawer.get_max_num_space())
            # pos_to_insert = minimum[1]
            # col = minimum[2]
            # print(f"Time {self.env.now:5.2f} - Start vertical move")
            # yield self.env.process(self.__vertical_move(drawer_entry.get_pos_y(), pos_to_insert))

            # print(f"Time {self.env.now:5.2f} - Start load a drawer")
            # yield self.env.process(self.__load(col, drawer, pos_to_insert))

            # col.remove_drawer(drawer)

            # print(f"Time {self.env.now:5.2f} - Start unload the floor")
            # yield self.env.process(self.__unload())

            # print(f"Time {self.env.now:5.2f} - Start vertical move")

            # print(f"Time {self.env.now:5.2f} - Start return to the hole")

            # print(f"Time {self.env.now:5.2f} - Ready to use!")
