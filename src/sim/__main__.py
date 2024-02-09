from sim.warehouse import Warehouse
from sim.utils.save_warehouse_state import save_config
import random


def work(sad: int = None):
    if sad is not None:
        random.seed(sad)

    # gen Warehouse
    warehouse = Warehouse()

    # run simulation
    warehouse.run_simulation()

    # save the configuration at the end
    save_config(warehouse.get_simulation().get_warehouse())

if __name__ == "__main__":
    work()
    # to find any error - brutal force
    # seed: int = 1000
    # while seed <= 10_000:
    #     try:
    #         work(seed)
    #     except Exception as e:
    #         print(f'SEED: {seed}')
    #         exit(1)
    #     seed += 1

# OLD ERRORS:
# AttributeError: 'EmptyEntry' object has no attribute 'get_drawer'
# work(705, 10000)

# AttributeError: 'int' object has no attribute 'offset_x'
# work(4, 100)

# Collision!: remove_drawer doesn't work properly
# work(4999)
