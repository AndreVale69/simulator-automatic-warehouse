from src.warehouse import Warehouse
from src.drawer import Drawer
from src.material import Material

# create warehouse
material = Material(123, "name", 256, 789, 12345)
material2 = Material(234, "abc", 564, 987, 00000)
drawer = Drawer([material, material2])
warehouse = Warehouse(1000)

# add a drawer to a warehouse

warehouse.add_drawer(drawer)
