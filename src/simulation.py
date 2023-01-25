import copy

import simpy
from simpy import Environment

from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse


class Simulation(object):
    def __init__(self, env: Environment, warehouse: Warehouse):
        from src.status_warehouse.Simulate_Events.buffer import Buffer

        self.env = env
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)

        self.buffer = Buffer(self.env, self.get_warehouse(), self)

        # -----: deve essere passata da Warehouse la sequenza

        # -----: send_back prende dalla baia il drawer e lo manda all'interno del magazzino usando Move
        # -----: extract_drawer prende un cassetto dentro il magazzino e lo mette nel carousel
        # -----: ComeBackToDeposit viene forzata dopo ogni operazione per ritornare al punto di partenza
        # -----: InsertMaterial classe abs che ha come figli InsertRandomMaterial e InsertMaterial

        # communication channel
        self.comm_chan = simpy.Store(env)
        # semaphore to
        self.semaphore_carousel = simpy.Resource(env, capacity=1)

    def simulate_actions(self, action_list: list[Action]):
        # an action can be a: MoveDrawer, InsertMaterial, RemoveMaterial, ExtractDrawerInBay, RemoveDrawerFromBay, etc.
        # run "control of buffer" process
        self.env.process(self.get_buffer().simulate_action())
        # run the actions
        for action in action_list:
            yield self.env.process(action.simulate_action())
        print(f"Time {self.env.now:5.2f} - Finish")

    def get_warehouse(self) -> Warehouse:
        return self.warehouse

    def get_comm_chan(self) -> simpy.Store:
        return self.comm_chan

    def get_semaphore_carousel(self) -> simpy.Resource:
        return self.semaphore_carousel

    def get_buffer(self):
        return self.buffer
