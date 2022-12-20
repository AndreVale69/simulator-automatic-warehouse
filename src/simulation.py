import copy
from simpy import Environment

from src.warehouse import Warehouse
from src.status_warehouse.Simulate_Events.action import Action


class Simulation(object):
    def __init__(self, env: Environment, warehouse: Warehouse):
        from src.status_warehouse.Simulate_Events.insert_material import InsertMaterial
        from src.status_warehouse.Simulate_Events.unload_drawer import UnloadDrawer
        from src.status_warehouse.Simulate_Events.buffer import Buffer
        from src.status_warehouse.Simulate_Events.go_to_deposit_drawer import GoToDepositDrawer
        from src.status_warehouse.Simulate_Events.load_drawer import LoadDrawer
        from src.status_warehouse.Simulate_Events.come_back_to_deposit import ComeBackToDeposit

        self.env = env
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)

        self.buffer = Buffer(self.env, self.get_warehouse(), self)

        self.insert_material_and_alloc_drawer = [InsertMaterial(self.env, self.get_warehouse(), self),
                                                 UnloadDrawer(self.env, self.get_warehouse(), self),
                                                 GoToDepositDrawer(self.env, self.get_warehouse(), self),
                                                 LoadDrawer(self.env, self.get_warehouse(), self),
                                                 ComeBackToDeposit(self.env, self.get_warehouse(), self)]
        # self.tmp = 2
        # self.machine = simpy.Resource(env, self.tmp)

    def simulate_actions(self, action_list: list[Action]):
        # an action can be a: MoveDrawer, InsertMaterial, RemoveMaterial, ExtractDrawerInBay, RemoveDrawerFromBay, etc.
        # active control of Buffer
        self.env.process(self.buffer.simulate_action())
        # execute the operations
        for action in action_list:
            yield self.env.process(action.simulate_action())

    #
    # def simulate_action(self, action: Action):
    #     # special case: two extract drawer in sequence
    #     #               1) standard execution
    #     #               2) second drawer goes into the buffer
    #     #               3) wait empty tray by running a new process for the second drawer
    #     return action.simulate(self)

    def get_warehouse(self) -> Warehouse:
        return self.warehouse

    # def get_machine(self):
    #     return self.machine
