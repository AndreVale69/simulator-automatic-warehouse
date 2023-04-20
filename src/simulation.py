import copy

import simpy
from simpy import Environment
from src.warehouse import Warehouse


# -----: send_back prende dalla baia il drawer e lo manda all'interno del magazzino usando Move
# -----: extract_drawer prende un cassetto dentro il magazzino e lo mette nel carousel
# -----: GoToDeposit viene forzata dopo ogni operazione per ritornare al punto di partenza
# -----: InsertMaterial classe abs che ha come figli InsertRandomMaterial e InsertMaterial


class Simulation:
    def __init__(self, env: Environment, warehouse: Warehouse):
        self.env = env
        # start the move process everytime an instance is created.
        self.warehouse = copy.deepcopy(warehouse)

        # allocation of carousel resources
        self.res_buffer = simpy.Resource(env, capacity=1)
        self.res_deposit = simpy.Resource(env, capacity=1)

    def simulate_actions(self, events_generated: list):
        from src.status_warehouse.enum_warehouse import EnumWarehouse
        from src.status_warehouse.Simulate_Events.buffer import Buffer
        from src.status_warehouse.Simulate_Events.send_back_drawer import SendBackDrawer
        from src.status_warehouse.Simulate_Events.extract_drawer import ExtractDrawer
        from src.status_warehouse.Simulate_Events.Material.InsertMaterial.insert_random_material \
            import InsertRandomMaterial
        from src.status_warehouse.Simulate_Events.Material.RemoveMaterial.remove_random_material \
            import RemoveRandomMaterial

        # run "control of buffer" process
        yield self.env.process(Buffer(self.env, self.get_warehouse(), self).simulate_action())

        # exec all events
        for index, event in enumerate(events_generated):
            match event:
                case "send_back":
                    print(f"~ Operation #{index} ~")
                    action = SendBackDrawer(self.get_environment(), self.get_warehouse(), self,
                                            EnumWarehouse.COLUMN)
                    yield self.env.process(action.simulate_action())
                    print(f"Time {self.env.now:5.2f} - FINISH SEND_BACK\n")

                case "extract_drawer":
                    print(f"~ Operation #{index} ~")
                    action = ExtractDrawer(self.get_environment(), self.get_warehouse(), self,
                                           EnumWarehouse.CAROUSEL)
                    yield self.env.process(action.simulate_action())
                    print(f"Time {self.env.now:5.2f} - FINISH EXTRACT_DRAWER\n")

                case "ins_mat":
                    print(f"~ Operation #{index} ~")
                    action = InsertRandomMaterial(self.get_environment(), self.get_warehouse(), self, duration=2)
                    yield self.env.process(action.simulate_action())
                    print(f"Time {self.env.now:5.2f} - FINISH INS_MAT\n")

                case "rmv_mat":
                    print(f"~ Operation #{index} ~")
                    action = RemoveRandomMaterial(self.get_environment(), self.get_warehouse(), self, duration=2)
                    yield self.env.process(action.simulate_action())
                    print(f"Time {self.env.now:5.2f} - FINISH RMV_MAT\n")

        print(f"Time {self.env.now:5.2f} - Finish simulation")

    def get_environment(self) -> simpy.Environment:
        return self.env

    def get_warehouse(self) -> Warehouse:
        return self.warehouse

    def get_res_buffer(self) -> simpy.Resource:
        return self.res_buffer

    def get_res_deposit(self) -> simpy.Resource:
        return self.res_deposit
