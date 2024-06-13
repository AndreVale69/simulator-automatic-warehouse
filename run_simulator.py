from time import sleep

from simulation.simulation_type.warehouse_simulation import WarehouseSimulation
from src.warehouse import Warehouse


def run_simulator():
    # gen warehouse and run simulation
    warehouse = Warehouse()
    simulation = WarehouseSimulation(warehouse)
    simulation.run_simulation()

if __name__ == '__main__':
    run_simulator()
    sleep(100000)