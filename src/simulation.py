import copy
import random

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

    # def simulate_actions(self, action_list: list[Action]):
    #     # an action can be a: MoveDrawer, InsertMaterial, RemoveMaterial, ExtractDrawerInBay, RemoveDrawerFromBay, etc.
    #     # run "control of buffer" process
    #     self.env.process(self.get_buffer().simulate_action())
    #     # run the actions
    #     for action in action_list:
    #         yield self.env.process(action.simulate_action())
    #     print(f"Time {self.env.now:5.2f} - Finish")

    def simulate_actions(self, alias_list: list, num_send_back, num_extract_drawer, num_ins_mat):
        from src.status_warehouse.Entry.drawerEntry import DrawerEntry
        from src.status_warehouse.enum_warehouse import EnumWarehouse
        from src.status_warehouse.Simulate_Events.send_back_drawer import SendBackDrawer
        from src.status_warehouse.Simulate_Events.extract_drawer import ExtractDrawer
        from src.status_warehouse.Simulate_Events.Material.InsertMaterial.insert_random_material import InsertRandomMaterial
        # run "control of buffer" process
        self.env.process(self.get_buffer().simulate_action())
        # calculate start balance of wh
        balance_wh = 0
        if type(self.get_warehouse().get_carousel().get_deposit_entry()) is DrawerEntry:
            balance_wh += 1
        if type(self.get_warehouse().get_carousel().get_buffer_entry()) is DrawerEntry:
            balance_wh += 1
        # run the actions
        while (num_send_back + num_extract_drawer + num_ins_mat) > 0:
            select_event = random.choice(alias_list)
            match select_event:
                case "send_back":
                    if 0 < balance_wh <= 2 and num_send_back > 0:
                        action = SendBackDrawer(self.get_environment(), self.get_warehouse(), self,
                                                self.get_warehouse().get_carousel().get_deposit_entry().get_drawer(),
                                                EnumWarehouse.COLUMN.name)
                        yield self.env.process(action.simulate_action())
                        print(f"\nTime {self.env.now:5.2f} - FINISH SEND_BACK\n")
                        balance_wh -= 1
                        num_send_back -= 1

                case "extract_drawer":
                    if 0 <= balance_wh < 2 and num_extract_drawer > 0:
                        # take a drawer
                        drawer = self.get_warehouse().choice_random_drawer()
                        action = ExtractDrawer(self.get_environment(), self.get_warehouse(), self, drawer,
                                               EnumWarehouse.CAROUSEL.name)
                        yield self.env.process(action.simulate_action())
                        print(f"\nTime {self.env.now:5.2f} - FINISH EXTRACT_DRAWER\n")
                        balance_wh += 1
                        num_extract_drawer -= 1

                case "ins_mat":
                    if 0 < balance_wh <= 2 and num_ins_mat > 0:
                        action = InsertRandomMaterial(self.get_environment(), self.get_warehouse(), self, duration=2)
                        yield self.env.process(action.simulate_action())
                        print(f"\nTime {self.env.now:5.2f} - FINISH INS_MAT\n")
                        num_ins_mat -= 1
        print(f"Time {self.env.now:5.2f} - Finish simulation")

    def get_environment(self) -> simpy.Environment:
        return self.env

    def get_warehouse(self) -> Warehouse:
        return self.warehouse

    def get_comm_chan(self) -> simpy.Store:
        return self.comm_chan

    def get_semaphore_carousel(self) -> simpy.Resource:
        return self.semaphore_carousel

    def get_buffer(self):
        return self.buffer
