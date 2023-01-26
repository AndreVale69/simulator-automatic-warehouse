from src.drawer import Drawer
from src.material import Material
from src.warehouse import Warehouse, save_config

warehouse = Warehouse()

material = Material(123, "name1", 150, 789, 12345)
material2 = Material(234, "name2", 126, 987, 00000)
material3 = Material(567, "name3", 100, 123, 45678)
# drawer = Drawer([material, material2])
drawer = Drawer()
drawer2 = Drawer([material3])

warehouse.get_carousel().add_drawer(drawer)
# warehouse.get_carousel().add_drawer(drawer2)

warehouse.gen_rand(8, 0)

# wh2 = copy.deepcopy(warehouse)
warehouse.run_simulation(400)

save_config(warehouse.get_simulation().get_warehouse())

