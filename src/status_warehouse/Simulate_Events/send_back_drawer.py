from simpy import Environment

from src.simulation import Simulation
from src.status_warehouse.Simulate_Events.Move.come_back_to_deposit import ComeBackToDeposit
from src.status_warehouse.Simulate_Events.Move.load import Load
from src.status_warehouse.Simulate_Events.Move.move import Move
from src.status_warehouse.Simulate_Events.Move.unload import Unload
from src.status_warehouse.Simulate_Events.Move.vertical import Vertical
from src.warehouse import Warehouse, Drawer


class SendBackDrawer(Move):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation, drawer: Drawer,
                 destination):
        super().__init__(env, warehouse, simulation, drawer, destination)

    def simulate_action(self):
        # TODO: implementare coordinata y del floor in warehouse
        with self.get_simulation().get_semaphore_carousel().request() as req:
            yield req
            # unloading drawer
            yield self.env.process(Unload(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                          self.get_destination()).simulate_action())
        # move the floor
        yield self.env.process(Vertical(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                        self.get_destination()).simulate_action())
        # loading drawer
        yield self.env.process(Load(self.get_env(), self.get_warehouse(), self.get_simulation(), self.get_drawer(),
                                    self.get_destination()).simulate_action())
        # force to come back to deposit
        # TODO: ComeBackToDeposit solo se c'è un cassetto, altrimenti lascio il floor lì (salvo coordinata y)
        yield self.env.process(ComeBackToDeposit(self.get_env(), self.get_warehouse(), self.get_simulation(),
                                                 self.get_drawer(), self.get_destination()).simulate_action())
