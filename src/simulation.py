import copy

from simpy import Environment
from src.warehouse import Warehouse
from src.drawer import Drawer


class Floor(object):
    def __init__(self, env: Environment, warehouse: Warehouse):
        self.env = env
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)
        self.pos_x = None
        self.pos_y = None

    def simulate_actions(self, action_list: list[Action]):
        # an action can be a: MoveDrawer, InsertMaterial, RemoveMaterial, ExtractDrawerInBay, RemoveDrawerFromBay, etc.
        for action in action_list:
            yield simulate_action(action)
        return

    def simulate_action(self, action: Action):
        # special case: two extract drawer in sequence
        #               1) standard execution
        #               2) second drawer goes into the buffer
        #               3) wait empty tray by running a new process for the second drawer
        return action.simulate(self)

    def get_warehouse(self) -> Warehouse:
        return self.warehouse

    def insert(self, drawer: Drawer): # called from RemoveDrawerFromBay
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

        # check if there is a drawer in the deposit
        if self.get_warehouse().check_deposit():
            print(f"Time {self.env.now:5.2f} - Start come back to deposit position")
            yield self.env.process(self.get_warehouse().come_back_to_deposit(drawer))

        print(f"Time {self.env.now:5.2f} - Finish")

    def remove(self):
        print("Remove")

    def search_material(self):
        print("Search")
        print("Insert or Remove")

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y
