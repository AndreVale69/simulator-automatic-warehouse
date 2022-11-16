import copy

import simpy

from src.warehouse import Warehouse
from src.drawer import Drawer
from src.material import Material
from src.simulation import Floor
from src.useful_func import obt_value_json
from src.status_warehouse.Container.column import Column

# # create warehouse
# warehouse = Warehouse()
#
# material = Material(123, "name", 256, 789, 12345)
# material2 = Material(234, "abc", 126, 987, 00000)
# drawer = Drawer([material, material2])
#
# material3 = Material(567, "def", 128, 564, 0)
# drawer2 = Drawer([material3])
#
# material4 = Material(890, "ghi", 75, 564, 0)
# # Trigger error with this line:
# # material4 = Material(890, "ghi", 76, 564, 0, warehouse.get_height())
# drawer3 = Drawer([material4])
#
# # add a drawer to a warehouse
# print("Initial warehouse: ")
# warehouse.print_warehouse()
# print()
#
# print("Add first drawer: ")
# warehouse.add_drawer(drawer)
# warehouse.print_warehouse()
# print()
#
# print("Add second drawer: ")
# warehouse.add_drawer(drawer2)
# warehouse.print_warehouse()
# print()
#
# print("Add third drawer: ")
# warehouse.add_drawer(drawer3)
# warehouse.print_warehouse()
# print()
#
# print("Remove first drawer: ")
# warehouse.remove_drawer(drawer)
# warehouse.print_warehouse()
# print()
#
# print("Remove third drawer: ")
# warehouse.remove_drawer(drawer3)
# warehouse.print_warehouse()
# print()
#
# print("Re-Add third drawer: ")
# warehouse.add_drawer(drawer3)
# warehouse.print_warehouse()
# print()
#
# print("Re-Add first drawer: ")
# warehouse.add_drawer(drawer)
# warehouse.print_warehouse()
# print()
#
# print("Remove second drawer: ")
# warehouse.remove_drawer(drawer2)
# warehouse.print_warehouse()
# print()
#
# print("Add new drawer (25 * 3): ")
# warehouse.add_drawer(Drawer([Material(147, "lmn", 75, 637, 0)]))
# warehouse.print_warehouse()
# print()
#
# print("Add new drawer (25 * 2): ")
# warehouse.add_drawer(Drawer([Material(258, "opq", 50, 103, 0)]))
# warehouse.print_warehouse()
# print()
#
# drawer7 = Drawer([Material(369, "rst", 125, 107, 0)])
# print("Add new drawer (25 * 5, change column!): ")
# warehouse.add_drawer(drawer7)
# warehouse.print_warehouse()
# print()
#
# print("Remove drawer of right column: ")
# warehouse.remove_drawer(drawer7)
# warehouse.print_warehouse()
# print()

# print("Add new drawer (25 * 1): ")
# warehouse.add_drawer(Drawer([Material(753, "uvz", 17, 346, 0, warehouse.get_height())]))
# warehouse.print_warehouse()
# print()
height = obt_value_json("height_warehouse")

warehouse = Warehouse()

container_right = Column(height, 0)
warehouse.add_container(container_right)
container_left = Column(height, 1)
warehouse.add_container(container_left)

material = Material(123, "name", 160, 789, 12345)
material2 = Material(234, "abc", 126, 987, 00000)
drawer = Drawer([material, material2])


containers = warehouse.get_container()
containers[0].add_drawer(5, drawer)
# containers[0].remove_drawer(drawer)

env = simpy.Environment()
floor = Floor(env, warehouse, drawer)
env.run(until=500)
