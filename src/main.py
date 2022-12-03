import copy

import simpy
from src.warehouse import Warehouse
from src.drawer import Drawer
from src.material import Material
from src.simulation import Floor
from src.status_warehouse.Container.column import Column

warehouse = Warehouse()

container_right = Column(0)
warehouse.add_container(container_right)
container_left = Column(1)
warehouse.add_container(container_left)

material = Material(123, "name", 160, 789, 12345)
material2 = Material(234, "abc", 126, 987, 00000)
drawer = Drawer([material, material2])

warehouse.get_carousel().add_drawer(True, drawer)
wh2 = copy.deepcopy(warehouse)

env = simpy.Environment()
floor = Floor(env, warehouse, drawer)
env.process(floor.insert(drawer))
env.run(until=10)
