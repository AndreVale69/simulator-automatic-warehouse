from __future__ import annotations

import copy
import random
from logging import getLogger

from automatic_warehouse.status_warehouse.material import Material
from automatic_warehouse.warehouse_configuration_singleton import (
    WarehouseConfigurationSingleton,
    WarehouseConfiguration,
    TrayConfiguration
)

logger = getLogger(__name__)


class Tray:
    """
    Representation of the tray (or tray) inside the warehouse.
    It contains all the information about the tray and the methods for add/remove a material, and so on.

    :type info: TrayConfiguration | None
    :type items: list[Material] | None
    :param info: configure the tray, leave ``None`` if you want to set the default (config) value.
    :param items: list of items to be added to the tray.
    """
    def __init__(self, info: TrayConfiguration | None = None, items: list[Material] | None = None):
        # items inside the tray
        config: WarehouseConfiguration = WarehouseConfigurationSingleton.get_instance().get_configuration()

        self.def_space: int = config.default_height_space
        self.first_trayEntry = None
        self.best_offset_x: None | int = None
        self.best_y: None | int = None
        if info is not None:
            self.length: int = info.length
            self.width: int = info.width
            self.height_limit: int = info.maximum_height
        else:
            self.length: int = config.tray.length
            self.width: int = config.tray.width
            self.height_limit: int = config.tray.maximum_height
        # TODO: create a custom data structure to store the items (such as a set)
        self.items: list[Material] = []
        self.height: None | int = None
        self.add_materials(copy.deepcopy(items if items is not None else []))

    def __eq__(self, other):
        return (
            isinstance(other, Tray) and
            self.items == other.items and
            self.height == other.height and
            self.num_space == other.num_space and
            self.first_trayEntry == other.first_trayEntry and
            self.length == other.length and
            self.width == other.width and
            self.height_limit == other.height_limit
        )

    def __hash__(self):
        return (
            12637 ^
            hash(tuple(self.items)) ^
            hash(self.height) ^
            hash(self.num_space) ^
            hash(self.length) ^
            hash(self.width) ^
            hash(self.height_limit)
        )

    def __deepcopy__(self, memo):
        copy_obj = Tray(TrayConfiguration(
            length=self.length,
            width=self.width,
            maximum_height=self.height_limit
        ), self.items)
        copy_obj.def_space = self.def_space
        copy_obj.height = self.height
        copy_obj.num_space = self.num_space
        copy_obj.best_offset_x = self.best_offset_x
        copy_obj.best_y = self.best_y
        copy_obj.length = self.length
        copy_obj.width = self.width
        return copy_obj

    def get_items(self) -> list[Material]:
        """
        Returns all the items inside the tray.

        :rtype: list[Material]
        :return: the list of items inside the tray.
        """
        return self.items

    def get_max_height(self) -> int:
        """
        Get the maximum height of the tray.

        :rtype: int
        :return: maximum height of a material inside tray.
        """
        return self.height

    def get_num_space_occupied(self) -> int:
        """
        Get the number of occupied spaces in the warehouse.

        :rtype: int
        :return: number of occupied spaces in the warehouse.
        """
        return self.num_space

    def get_first_tray_entry(self):
        """
        Get the first tray entry (object) inside the warehouse.

        :rtype: TrayEntry
        :return: first tray entry (object) inside the warehouse.
        """
        return self.first_trayEntry

    def get_best_offset_x(self) -> int:
        """
        Get the best offset x of the tray.

        :rtype: int
        :return: the best offset x of the tray.
        """
        return self.best_offset_x

    def get_best_y(self) -> int:
        """
        Get the best y of the tray.

        :rtype: int
        :return: the best y of the tray.
        """
        return self.best_y

    def get_length(self) -> int:
        """
        Get the length of the tray.

        :rtype: int
        :return: the length of the tray.
        """
        return self.length

    def get_width(self) -> int:
        """
        Get the width of the tray.

        :rtype: int
        :return: the width of the tray.
        """
        return self.width

    def get_height_limit(self) -> int:
        """
        Get the height limit of the tray.

        :rtype: int
        :return: the height limit of the tray.
        """
        return self.height_limit

    def get_num_materials(self) -> int:
        """
        Get the number of materials.

        :rtype: int
        :return: the number of materials.
        """
        return len(self.items)

    def add_material(self, material: Material):
        """
        Add a material to the tray.
        
        Note: The material to be added should respect the following rules:
        
        1. width smaller than the width of the tray;
        
        2. height less than the maximum height of the tray (``maximum_height`` field in the configuration);
        
        3. length less than the length of the tray.

        :type material: Material
        :param material: material to be added to the tray.
        :raises ValueError: if the material it is too large.
        """
        if not (material.width < self.width and material.height < self.height_limit and material.length < self.length):
            logger.error("The material cannot be added to the tray because it is too large.")
            raise ValueError
        # insert in tail
        self.items.append(material)
        self.__calculate_max_height()

    def add_materials(self, materials: list[Material]):
        """
        Add materials to the tray.

        Note: Each material to be added should respect the following rules:
        
        1. width smaller than the width of the tray;
        
        2. height less than the maximum height of the tray (``maximum_height`` field in the configuration);
        
        3. length less than the length of the tray.

        :type materials: list[Material]
        :param materials: materials to be added to the tray.
        :raises ValueError: if the materials are too large.
        """
        for material in materials:
            if not (
                material.width < self.width and
                material.height < self.height_limit and
                material.length < self.length
            ):
                logger.error("The material cannot be added to the tray because it is too large.")
                raise ValueError
            self.items.append(material)
        self.__calculate_max_height()


    def remove_material(self, material: Material):
        """
        Remove a material from the tray.

        :type material: Material
        :param material: material to be removed from the tray.
        """
        self.items.remove(material)
        self.__calculate_max_height()

    def remove_materials(self, materials: list[Material]):
        """
        Remove materials from the tray.

        :type materials: list[Material]
        :param materials: materials to be removed from the tray.
        """
        for material in materials:
            self.items.remove(material)
        self.__calculate_max_height()

    def set_first_tray_entry(self, tray_entry):
        """
        Set the first tray entry (object).

        It is a pointer to the first entry in the tray, 
        used in a clever way to avoid iterating over the list.

        :type tray_entry: TrayEntry
        :param tray_entry: the first tray entry pointer.
        """
        self.first_trayEntry = tray_entry

    def set_best_offset_x(self, offset_x: int):
        """
        Set the best offset x of the tray.

        :type offset_x: int
        :param offset_x: offset x of the tray.
        """
        self.best_offset_x = offset_x

    def set_best_y(self, pos_y: int):
        """
        Set the best offset y of the tray.

        :type pos_y: int
        :param pos_y: offset y of the tray.
        """
        self.best_y = pos_y

    def __calculate_max_height(self):
        """
        Private method to calculate the height of a tray 
        after an insert or remove a material.
        """
        def_space, materials = self.def_space, self.items

        # if there are no materials, use the default space
        # otherwise, calculate the maximum height and how many entries are occupied
        self.height = max([material.get_height() for material in materials], default=def_space)
        self.num_space = self.height // def_space
        # odd, approx the next
        if (self.height % def_space) != 0: self.num_space += 1



def gen_rand_trays(how_many: int, materials_to_insert: list[Material], info: TrayConfiguration | None = None) -> list[Tray]:
    """
    Static method to generate random trays.

    :type how_many: int
    :type materials_to_insert: list[Material]
    :type info: TrayConfiguration | None
    :rtype: list[Tray]
    :param how_many: how many trays to generate.
    :param materials_to_insert: a list of materials to insert.
    :param info: information about the tray, leave ``None`` if you want to set the default (config) value.
    :return: the generated trays list.
    """
    trays: list[Tray] = []
    materials_to_insert = copy.deepcopy(materials_to_insert)
    # for i in range(how_many):
    for _ in range(how_many):
        # select a random material if there are materials, otherwise None
        random_material: Material | None = random.choice(materials_to_insert) if len(materials_to_insert) > 0 else None
        # create a random tray with a random material
        trays.append(gen_rand_tray(info, random_material))
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
        # select a random tray
        random_tray: Tray = random.choice(trays)
        # add random material inside a random tray
        random_tray.add_material(random_material)
        # remove the material just added
        materials_to_insert.remove(random_material)
    return trays

def gen_rand_tray(info: TrayConfiguration = None, material_to_insert: Material = None) -> Tray:
    """
    Static method to generate a random tray.

    :type info: TrayConfiguration
    :type material_to_insert: Material
    :rtype: Tray
    :param info: the tray configuration, leave ``None`` if you want to set the default (config) value.
    :param material_to_insert: a material to insert.
    :return: the generated tray.
    """
    return Tray(info, [material_to_insert] if material_to_insert is not None else material_to_insert)
