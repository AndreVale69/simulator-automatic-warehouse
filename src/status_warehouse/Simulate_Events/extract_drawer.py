from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.buffer import Buffer
from src.status_warehouse.Simulate_Events.Move.come_back_to_deposit import ComeBackToDeposit
from src.status_warehouse.Simulate_Events.Move.go_to_buffer import GoToBuffer
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.status_warehouse.Simulate_Events.Move.unload import Unload
from src.status_warehouse.Simulate_Events.Move.vertical import Vertical
from src.warehouse import Warehouse, Drawer


class ExtractDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination):
        super().__init__(env, warehouse, simulation, drawer, destination)

    def simulate_action(self):
        # try to release the drawer in the deposit
        if self.get_simulation().get_res_deposit().count == 0:
            with self.get_simulation().get_res_deposit().request() as req:
                yield req
                yield self.env.process(self.actions(load_in_buffer=False))
        else:
            # if the deposit is under process by another one, release it inside the buffer
            with self.get_simulation().get_res_buffer().request() as req:
                yield req
                yield self.env.process(self.actions(load_in_buffer=True))

    def actions(self, load_in_buffer: bool):
        # move the floor
        yield self.env.process(Vertical(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                        self.get_destination()).simulate_action())
        # unloading drawer
        yield self.env.process(Unload(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                      self.get_destination()).simulate_action())
        # come back to the deposit
        if load_in_buffer:
            yield self.env.process(GoToBuffer(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                              self.get_drawer(), self.get_destination()).simulate_action())
        else:
            yield self.env.process(ComeBackToDeposit(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                                     self.get_drawer(), self.get_destination()).simulate_action())
        print(f"Time {self.env.now:5.2f} - Start to load in the carousel")
        yield self.env.process(self.get_warehouse().load_in_carousel(self.get_drawer(), self.get_destination(),
                                                                     load_in_buffer=load_in_buffer))

        # TODO: to opt!
        if load_in_buffer:
            # exec Buffer process
            self.env.process(Buffer(self.get_env(), self.get_warehouse(), self.get_simulation()).simulate_action())
            # check ComeBackToDeposit move
            super().simulate_action()
