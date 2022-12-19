from simpy import Environment
from src.status_warehouse.Simulate_Events.action import Action
from src.warehouse import Warehouse
from src.drawer import Drawer
# from src.simulation import Floor


class InsertDrawerInWarehouse(Action):
    def __init__(self, env: Environment, warehouse: Warehouse, floor):
        super().__init__(env, warehouse, floor)

    # override
    def simulate_action(self, drawer: Drawer):
        from src.status_warehouse.Simulate_Events.insert_material import InsertMaterial
        from src.status_warehouse.Simulate_Events.unload_drawer import UnloadDrawer
        from src.status_warehouse.Simulate_Events.show_buffer import ShowBuffer

        yield self.env.process(InsertMaterial(self.env, self.warehouse, self.floor).simulate_action())

        yield self.env.process(UnloadDrawer(self.env, self.warehouse, self.floor).simulate_action(drawer))

        # check if the buffer is to load or not
        # if self.get_warehouse().check_buffer():
        self.env.process(ShowBuffer(self.env, self.warehouse, self.floor).simulate_action())

        # move the floor
        print(f"Time {self.env.now:5.2f} - Start vertical move")
        yield self.env.process(self.get_warehouse().allocate_best_pos(drawer))

        # add the drawer
        print(f"Time {self.env.now:5.2f} - Start loading a drawer")
        yield self.env.process(self.get_warehouse().load(drawer))

        print(f"Time {self.env.now:5.2f} - Start come back to deposit position")
        yield self.env.process(self.get_warehouse().come_back_to_deposit(drawer))

        # check if there is a drawer in the deposit
        if self.get_warehouse().check_deposit():
            # bay now is out
            print(f"Time {self.env.now:5.2f} - Start to show the bay")
            yield self.env.timeout(self.get_warehouse().horiz_move(0))

        print(f"Time {self.env.now:5.2f} - ~ Finish insertDrawerInWarehouse ~")
