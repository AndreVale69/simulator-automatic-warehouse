import random
import uuid


class Material:
    def __init__(self, barcode: hex, name: str, height: int, length: int, width: int):
        """

        :param barcode: unique id of a material
        :param name: name of a material
        :param height: height of a material
        :param length: length of a material
        :param width: width of a material
        """
        from src.useful_func import open_config

        # maximum height of a material to fit into a drawer
        config: dict = open_config()
        max_height_material = config["carousel"]["buffer_height"]

        # check height of a material
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
        """Overrides the default implementation"""
        if isinstance(other, Material):
            return self.get_barcode() == other.get_barcode() and \
                self.get_name() == other.get_name() and \
                self.get_height() == other.get_height() and \
                self.get_length() == other.get_length() and \
                self.get_width() == other.get_width()
        else:
            return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash((self.get_barcode(), self.get_name(), self.get_height(), self.get_length(), self.get_width()))

    def __deepcopy__(self, memo):
        copy_obj = Material(self.get_barcode(),
                            self.get_name(),
                            self.get_height(),
                            self.get_length(),
                            self.get_width())
        return copy_obj

    def get_barcode(self) -> int:
        return self.barcode

    def get_name(self) -> str:
        return self.name

    def get_height(self) -> int:
        return self.height

    def get_length(self) -> int:
        return self.length

    def get_width(self) -> int:
        return self.width


def gen_rand_materials(how_many: int, max_height: int = 50) -> list[Material]:
    materials: list[Material] = []
    for i in range(how_many):
        materials.append(gen_rand_material(max_height))
    return materials


def gen_rand_material(max_height: int = 50) -> Material:
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
    height = random.randint(25, max_height)
    length = random.randint(25, 150)
    width = random.randint(25, 150)

    return Material(barcode, name, height, length, width)
