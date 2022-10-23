from src.warehouse import Warehouse
from src.drawer import Drawer
from src.material import Material

# create warehouse
material = Material(123, "name", 256, 789, 12345)
material2 = Material(234, "abc", 564, 987, 00000)
drawer = Drawer()
warehouse = Warehouse()

drawer.add_material(material)
drawer.add_material(material2)
warehouse.add_drawer(drawer, 0)
drawer.print_array()
warehouse.print_warehouse()
