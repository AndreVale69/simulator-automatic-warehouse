import copy
import random

from src.sim.material import Material
from src.sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class Drawer:
    """
    Representation of the drawer (or tray) inside the warehouse.
    It contains all the information about the drawer and the methods for add/remove a material, and so on.
    """
    def __init__(self, items: list[Material] = None):
        # items inside the drawer
        config: dict = WarehouseConfigurationSingleton.get_instance().get_configuration()

        self.items = copy.deepcopy(items if items is not None else [])
        self.def_space = config["default_height_space"]
        self.__calculate_max_height()

        self.first_drawerEntry = None
        self.best_offset_x = None
        self.best_y = None

    def __eq__(self, other):
        return (
            isinstance(other, Drawer) and
            self.get_items() == other.get_items() and
            self.get_max_height() == other.get_max_height() and
            self.get_max_num_space() == other.get_max_num_space() and
            self.get_first_drawerEntry() == other.get_first_drawerEntry()
        )

    def __hash__(self):
        return (
            13 ^
            hash(tuple(self.get_items())) ^
            hash(self.get_max_height()) ^
            hash(self.get_max_num_space()) ^
            hash(self.get_first_drawerEntry())
        )

    def __deepcopy__(self, memo):
        copy_obj = Drawer(self.get_items())
        # copy_obj.items = copy.deepcopy(self.get_items(), memo)
        copy_obj.def_space = self.__get_def_space()
        copy_obj.max_height = self.get_max_height()
        copy_obj.num_space = self.get_max_num_space()
        copy_obj.best_offset_x = self.get_best_offset_x()
        copy_obj.best_y = self.get_best_y()
        return copy_obj

    def get_items(self) -> list[Material]:
        """
        Returns all the items inside the drawer.

        :rtype: list[Material]
        :return: the list of items inside the drawer
        """
        return self.items

    def get_max_height(self) -> int:
        """
        Get the maximum height of the drawer.

        :rtype: int
        :return: maximum height of a material inside drawer
        """
        return self.max_height

    def get_max_num_space(self) -> int:
        """
        Get the number of occupied spaces in the warehouse.

        :rtype: int
        :return: number of occupied spaces in the warehouse
        """
        return self.num_space

    def get_first_drawerEntry(self):
        """
        Get the first drawer entry (object) inside the warehouse.

        :rtype: DrawerEntry
        :return: first drawer entry (object) inside the warehouse
        """
        return self.first_drawerEntry

    def get_best_offset_x(self) -> int:
        """
        Get the best offset x of the drawer.

        :rtype: int
        :return: the best offset x of the drawer
        """
        return self.best_offset_x

    def get_best_y(self) -> int:
        """
        Get the best y of the drawer.

        :rtype: int
        :return: the best y of the drawer
        """
        return self.best_y

    def get_num_materials(self) -> int:
        """
        Get the number of materials.

        :rtype: int
        :return:
        """
        return len(self.items)

    def add_material(self, material: Material):
        """
        Add a material to the drawer.

        :type material: Material
        :param material: material to be added to the drawer.
        """
        # insert in tail
        self.get_items().append(material)
        self.__calculate_max_height()

    def remove_material(self, material: Material):
        """
        Remove a material from the drawer.

        :type material: Material
        :param material: material to be removed from the drawer.
        """
        # remove
        self.items.remove(material)
        self.__calculate_max_height()

    def set_first_drawerEntry(self, drawer_entry):
        """
        Set the first drawer entry (object).
        It is a pointer to the first entry in the drawer, used in a clever way to avoid iterating over the list.

        :type drawer_entry: DrawerEntry
        :param drawer_entry: the first drawer entry pointer.
        """
        self.first_drawerEntry = drawer_entry

    def set_best_offset_x(self, offset_x: int):
        """
        Set the best offset x of the drawer.

        :type offset_x: int
        :param offset_x: offset x of the drawer.
        """
        self.best_offset_x = offset_x

    def set_best_y(self, pos_y: int):
        """
        Set the best offset y of the drawer.

        :type pos_y: int
        :param pos_y: offset y of the drawer.
        """
        self.best_y = pos_y

    def __get_def_space(self) -> int:
        """
        Get the default space of the drawer.

        :rtype: int
        :return: the default space of the drawer.
        """
        return self.def_space

    def __calculate_max_height(self):
        """
        Private method to calculate the height of a drawer after an insert o remove a material.
        """
        def_space = self.__get_def_space()
        materials = self.get_items()

        # if there are no materials, use the default space
        # otherwise, calculate the maximum height and how many entries are occupied
        self.max_height = max([material.get_height() for material in materials], default=def_space)
        self.num_space = self.max_height // def_space
        if (self.max_height % def_space) != 0:
            # odd, approx the next
            self.num_space += 1



def gen_rand_drawers(how_many: int, materials_to_insert: list[Material]) -> list[Drawer]:
    """
    Static method to generate random drawers.

    :type how_many: int
    :type materials_to_insert: list[Material]
    :rtype: list[Drawer]
    :param how_many: how many drawers to generate.
    :param materials_to_insert: a list of materials to insert.
    :return: the generated drawers list.
    """
    drawers: list[Drawer] = []
    materials_to_insert = copy.deepcopy(materials_to_insert)
    # for i in range(how_many):
    for _ in range(how_many):
        # select a random material if there are materials, otherwise None
        random_material: Material | None = random.choice(materials_to_insert) if len(materials_to_insert) > 0 else None
        # create a random drawer with a random material
        drawers.append(gen_rand_drawer(random_material))
        # remove the material just added
        try:
            materials_to_insert.remove(random_material)
        except ValueError:
            # no random material chosen, random_material is None
            continue
    # if there are some materials yet
    while len(materials_to_insert) != 0:
        # select a random material
        random_material: Material = random.choice(materials_to_insert)
        # select a random drawer
        random_drawer: Drawer = random.choice(drawers)
        # add random material inside a random drawer
        random_drawer.add_material(random_material)
        # remove the material just added
        materials_to_insert.remove(random_material)
    return drawers

def gen_rand_drawer(material_to_insert: Material = None) -> Drawer:
    """
    Static method to generate a random drawer.

    :type material_to_insert: Material
    :rtype: Drawer
    :param material_to_insert: a material to insert.
    :return: the generated drawer.
    """
    return Drawer([material_to_insert] if material_to_insert is not None else None)
