from simpy import Environment
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
from src.drawer import Drawer
# from src.simulation import Floor


class InsertDrawerInWarehouse(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self, drawer: Drawer = None):
        from src.status_warehouse.Simulate_Events.insert_material import InsertMaterial
        from src.status_warehouse.Simulate_Events.unload_drawer import UnloadDrawer
        from src.status_warehouse.Simulate_Events.buffer import Buffer
        from src.status_warehouse.Simulate_Events.go_to_deposit_drawer import GoToDepositDrawer
        from src.status_warehouse.Simulate_Events.load_drawer import LoadDrawer
        from src.status_warehouse.Simulate_Events.come_back_to_deposit import ComeBackToDeposit

        yield self.env.process(InsertMaterial(self.env, self.warehouse, self.floor).simulate_action())

        yield self.env.process(UnloadDrawer(self.env, self.warehouse, self.floor).simulate_action(drawer))

        self.env.process(Buffer(self.env, self.warehouse, self.floor).simulate_action())

        yield self.env.process(GoToDepositDrawer(self.env, self.warehouse, self.floor).simulate_action(drawer))

        yield self.env.process(LoadDrawer(self.env, self.warehouse, self.floor).simulate_action(drawer))

        yield self.env.process(ComeBackToDeposit(self.env, self.warehouse, self.floor).simulate_action(drawer))

        print(f"Time {self.env.now:5.2f} - ~ Finish insertDrawerInWarehouse ~")
