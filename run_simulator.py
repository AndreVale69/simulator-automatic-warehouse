from automatic_warehouse.simulation.simulation_type.warehouse_simulation import WarehouseSimulation
from automatic_warehouse.warehouse import Warehouse


def run_simulator():
    # gen warehouse and run simulation
    warehouse = Warehouse()
    simulation = WarehouseSimulation(warehouse)
    simulation.run_simulation()

if __name__ == '__main__':
    run_simulator()