import random
import uuid

from src.warehouse_configuration_singleton import WarehouseConfigurationSingleton


class Material:
    def __init__(self, barcode: hex, name: str, height: int, length: int, width: int):
        """
        Class that represents a material that can be found inside a tray.

        :type barcode: hex
        :type name: str
        :type height: int
        :type length: int
        :type width: int
        :param barcode: unique ID of a material.
        :param name: name of a material.
        :param height: height of a material.
        :param length: length of a material.
        :param width: width of a material.
        """
        # maximum height of a material to fit into a tray
        max_height_material = WarehouseConfigurationSingleton.get_instance().get_configuration().carousel.buffer_height

        # check the height of a material
        if height > max_height_material:
            raise ValueError("The height of element " +
                             name +
                             " is too high (max height: " +
                             str(max_height_material) + ")")

        self.barcode = barcode
        self.name = name
        self.height = height
        self.length = length
        self.width = width

    def __eq__(self, other):
        return (
            isinstance(other, Material) and
            self.get_barcode() == other.get_barcode() and
            self.get_name() == other.get_name() and
            self.get_height() == other.get_height() and
            self.get_length() == other.get_length() and
            self.get_width() == other.get_width()
        )

    def __hash__(self):
        return 13463 ^ hash((self.barcode, self.name, self.height, self.length, self.width))

    def __deepcopy__(self, memo):
        return Material(self.get_barcode(),
                        self.get_name(),
                        self.get_height(),
                        self.get_length(),
                        self.get_width())

    def get_barcode(self) -> int:
        """
        Get the barcode of the material.

        :rtype: int
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
    materials: list[Material] = []
    for i in range(how_many):
        materials.append(gen_rand_material(min_height, max_height))
    return materials


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
