from src.sim.warehouse import Warehouse


def run_simulator():
    # debug purpose
    # import random
    # random.seed(None)

    # gen warehouse and run simulation
    (warehouse := Warehouse()).run_simulation()

    # save the configuration at the end
    # from src.sim.utils.save_warehouse_state import save_config
    # save_config(warehouse.get_simulation().get_warehouse())


# OLD ERRORS:
# AttributeError: 'EmptyEntry' object has no attribute 'get_drawer'
# work(705, 10000)

# AttributeError: 'int' object has no attribute 'offset_x'
# work(4, 100)

# Collision!: remove_drawer doesn't work properly
# work(4999)
