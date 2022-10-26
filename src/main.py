from src.warehouse import Warehouse
from src.drawer import Drawer
from src.material import Material

# create warehouse
warehouse = Warehouse(500)

material = Material(123, "name", 256, 789, 12345, warehouse.get_height())
material2 = Material(234, "abc", 126, 987, 00000, warehouse.get_height())
drawer = Drawer([material, material2])

material3 = Material(567, "def", 128, 564, 0, warehouse.get_height())
drawer2 = Drawer([material3])

material4 = Material(890, "ghi", 75, 564, 0, warehouse.get_height())
# Trigger error with this line:
# material4 = Material(890, "ghi", 76, 564, 0, warehouse.get_height())
drawer3 = Drawer([material4])

# add a drawer to a warehouse
warehouse.print_warehouse()
warehouse.add_drawer(drawer)
warehouse.print_warehouse()
warehouse.add_drawer(drawer2)
warehouse.print_warehouse()
warehouse.add_drawer(drawer3)
warehouse.print_warehouse()
