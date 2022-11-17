class Material:
    def __init__(self, barcode: int, name: str, height: int, length: int, width: int):
        """

        :param barcode: unique id of a material
        :param name: name of a material
        :param height: height of a material
        :param length: length of a material
        :param width: width of a material
        """
        from src.useful_func import obt_value_json
        # maximum height of a material to fit into a drawer
        max_height_material = obt_value_json("hole_height")

        # check height of a material
        if height > max_height_material:
            raise ValueError("The height of element " +
                             name +
                             " is too high (max height: " +
                             str(max_height_material) + ")")

        self.__barcode = barcode
        self.__name = name
        self.__height = height
        self.__length = length
        self.__width = width

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

    def get_barcode(self) -> int:
        return self.__barcode

    def get_name(self) -> str:
        return self.__name

    def get_height(self) -> int:
        return self.__height

    def get_length(self) -> int:
        return self.__length

    def get_width(self) -> int:
        return self.__width
