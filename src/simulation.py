import copy

import simpy
from simpy import Environment

from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse


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

        # self.search_material_and_remove

        # communication channel
        self.comm_chan = simpy.Store(env)

    def simulate_actions(self, action_list: list[Action]):
        # an action can be a: MoveDrawer, InsertMaterial, RemoveMaterial, ExtractDrawerInBay, RemoveDrawerFromBay, etc.
        # run "control of buffer" process
        self.env.process(self.get_buffer().simulate_action())
        # run the actions
        for action in action_list:
            yield self.env.process(action.simulate_action())

    def get_warehouse(self) -> Warehouse:
        return self.warehouse

    def get_comm_chan(self):
        return self.comm_chan

    def get_buffer(self):
        return self.buffer
