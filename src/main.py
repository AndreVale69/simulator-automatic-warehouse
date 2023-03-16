from src.drawer import Drawer
from src.material import Material
from src.warehouse import Warehouse, save_config
import random

def work(sad, num_actions):
    random.seed(sad)

    warehouse = Warehouse()

    material = Material(hex(123), "name1", 150, 789, 12345)
    material2 = Material(hex(234), "name2", 126, 987, 00000)
    material3 = Material(hex(567), "name3", 100, 123, 45678)
    drawer = Drawer([material, material2])
    # drawer = Drawer()
    drawer2 = Drawer([material3])

    warehouse.get_carousel().add_drawer(drawer)
    warehouse.get_carousel().add_drawer(drawer2)

    warehouse.gen_rand(8, 0)

    # wh2 = copy.deepcopy(warehouse)
    warehouse.run_simulation(time=4000, num_actions=num_actions)

    save_config(warehouse.get_simulation().get_warehouse())

# AttributeError: 'EmptyEntry' object has no attribute 'get_drawer'
work(705, 10000)

# AttributeError: 'int' object has no attribute 'offset_x'
# work(4, 100)

# work(4, 100)
