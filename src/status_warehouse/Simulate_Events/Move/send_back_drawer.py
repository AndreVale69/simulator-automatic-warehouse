from simpy import Environment

from src.simulation import Simulation
from src.warehouse import Warehouse


# TODO: questa è una sottoclasse di Move
class UnloadDrawer(object):
    def __init__(self, env: Environment, warehouse: Warehouse, simulation: Simulation):
        self.env = env
        self.warehouse = warehouse
        self.simulation = simulation

    def get_env(self):
        return self.env

    def get_warehouse(self):
        return self.warehouse

    def get_simulation(self):
        return self.simulation

    def simulate_action(self):
        print(f"Time {self.env.now:5.2f} - Start unloading a drawer")
        # TODO: l'argomento è già nella classe warehouse
        # TODO: le righe vanno direttamente in warehouse
        # TODO: si prende il drawer come parametro
        # TODO: unload dipende se da carousel o da column. Nella prima eseguo check_buffer, else no
        # unloading drawer
        yield self.env.process(self.get_warehouse().unload(self.get_warehouse().get_drawer_of_support()))
        # remove only from container
        self.get_warehouse().get_carousel().remove_drawer(self.get_warehouse().get_drawer_of_support())
        # TODO: vanno in carousel
        # check if the buffer is full or empty
        if self.get_warehouse().check_buffer():
            # trigger buffer.py process
            self.get_simulation().get_comm_chan().put("Wake up buffer.py!")
