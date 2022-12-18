import copy

from simpy import Environment
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.status_warehouse.Simulate_Events.insertDrawerInWarehouse import InsertDrawerInWarehouse


class Floor(object):
    def __init__(self, env: Environment, warehouse: Warehouse):
        self.env = env
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)

    def insert(self, drawer: Drawer):
        return InsertDrawerInWarehouse(self.env, self.warehouse, self).simulate_action(drawer)

    # def simulate_actions(self, action_list: list[Action]):
    #      an action can be a: MoveDrawer, InsertMaterial, RemoveMaterial, ExtractDrawerInBay, RemoveDrawerFromBay, etc.
    #     for action in action_list:
    #         yield simulate_action(action)
    #     return
#
    # def simulate_action(self, action: Action):
    #     # special case: two extract drawer in sequence
    #     #               1) standard execution
    #     #               2) second drawer goes into the buffer
    #     #               3) wait empty tray by running a new process for the second drawer
    #     return action.simulate(self)

    def get_warehouse(self) -> Warehouse:
        return self.warehouse
