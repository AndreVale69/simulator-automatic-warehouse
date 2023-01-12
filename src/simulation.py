import copy

import simpy
from simpy import Environment

from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse


class Simulation(object):
    def __init__(self, env: Environment, warehouse: Warehouse):
        from src.status_warehouse.Simulate_Events.insert_random_material import InsertRandomMaterial
        from src.status_warehouse.Simulate_Events.buffer import Buffer
        from src.status_warehouse.Simulate_Events.come_back_to_deposit import ComeBackToDeposit
        from src.status_warehouse.Simulate_Events.Move.move import Move

        self.env = env
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)

        self.buffer = Buffer(self.env, self.get_warehouse(), self)

        self.insert_material_and_alloc_drawer = [InsertRandomMaterial(self.env, self.get_warehouse(), self, duration=2),
                                                 Move(self.env, self.get_warehouse(), self),
                                                 ComeBackToDeposit(self.env, self.get_warehouse(), self)]
        # TODO: send_back prende dalla baia il drawer e lo manda all'interno del magazzino usando Move
        # TODO: extract_drawer prende un cassetto dentro il magazzino e lo mette nel carousel
        # TODO: ComeBackToDeposit viene forzata dopo ogni operazione per ritornare al punto di partenza
        # TODO: InsertMaterial classe abs che ha come figli InsertRandomMaterial e InsertMaterial
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
