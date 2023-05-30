from sim.warehouse import Warehouse, save_config
import random


def work(sad: int = None):
    if sad is not None:
        random.seed(sad)

    # gen Warehouse
    warehouse = Warehouse()
    # value = random.randint(0, 10000)
    # random.seed(value)
    # with open("Output.txt", "w") as text_file:
    #    text_file.write(str(value))

    # run simulation
    warehouse.run_simulation()

    # save the configuration at the end
    save_config(warehouse.get_simulation().get_warehouse())


work()

# OLD ERRORS
# AttributeError: 'EmptyEntry' object has no attribute 'get_drawer'
# work(705, 10000)

# AttributeError: 'int' object has no attribute 'offset_x'
# work(4, 100)
