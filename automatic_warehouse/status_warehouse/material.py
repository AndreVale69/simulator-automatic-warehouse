import random
import uuid

from automatic_warehouse.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class Material:
    """
    Class that represents a material that can be found inside a tray.

    :type barcode: str
    :type name: str
    :type height: int
    :type length: int
    :type width: int
    :param barcode: unique ID of a material.
    :param name: name of a material.
    :param height: height of a material.
    :param length: length of a material.
    :param width: width of a material.
    :raises ValueError: if the specified height is greater than the maximum height of the tray (config value).
    """

    def __init__(self, barcode: str, name: str, height: int, length: int, width: int):
        # maximum height of a material to fit into a tray
        max_height_material = WarehouseConfigurationSingleton.get_instance().get_configuration().tray.maximum_height

        # check the height of a material
        if height > max_height_material:
            raise ValueError(f"The height of element {name} is too high (max height: {max_height_material})")

        self.barcode = barcode
        self.name = name
        self.height = height
        self.length = length
        self.width = width

    def __eq__(self, other):
        return (
            isinstance(other, Material) and
            self.barcode == other.barcode and
            self.name == other.name and
            self.height == other.height and
            self.length == other.length and
            self.width == other.width
        )

    def __hash__(self):
        return 13463 ^ hash((self.barcode, self.name, self.height, self.length, self.width))

    def __deepcopy__(self, memo):
        return Material(self.barcode, self.name, self.height, self.length, self.width)

    def get_barcode(self) -> str:
        """
        Get the barcode of the material.

        :rtype: str
        :return: the barcode of the material.
        """
        return self.barcode

    def get_name(self) -> str:
        """
        Get the name of the material.

        :rtype: str
        :return: the name of the material.
        """
        return self.name

    def get_height(self) -> int:
        """
        Get the height of the material.

        :rtype: int
        :return: the height of the material.
        """
        return self.height

    def get_length(self) -> int:
        """
        Get the length of the material.

        :rtype: int
        :return: the length of the material.
        """
        return self.length

    def get_width(self) -> int:
        """
        Get the width of the material.

        :rtype: int
        :return: the width of the material.
        """
        return self.width


def gen_rand_materials(how_many: int, min_height: int = 25, max_height: int = 50) -> list[Material]:
    """
    Static method to generate random materials.

    :type how_many: int
    :type min_height: int
    :type max_height: int
    :rtype: list[Material]
    :param how_many: how many materials to generate.
    :param min_height: the minimum height (lower limit) of the material.
    :param max_height: the maximum height (upper limit) of the materials.
    :return: the generated materials list.
    """
    return [gen_rand_material(min_height, max_height) for _ in range(how_many)]


def gen_rand_material(min_height: int = 25, max_height: int = 50) -> Material:
    """
    Static method to generate a random material.

    :type min_height: int
    :type max_height: int
    :rtype: Material
    :param min_height: the minimum height (lower limit) of the material.
    :param max_height: the maximum height (upper limit) of the material.
    :return: the material generated.
    """
    assert min_height <= max_height, "min_height must be less than max_height"
    assert min_height > 0, "min_height must be greater than 0"
    assert max_height > 0, "max_height must be greater than 0"
    name_materials = ['Shirt',
                      'Pasta',
                      'Tomato',
                      'Bottle',
                      'Tablet',
                      'Helmet']

    # UUID to avoid the same hex barcode
    barcode = uuid.uuid4().hex
    name = random.choice(name_materials)
    # height max is buffer height = 150
    height = random.randint(min_height, max_height)
    length = random.randint(25, 150)
    width = random.randint(25, 150)

    return Material(barcode, name, height, length, width)
