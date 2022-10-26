# TODO: improve this class
class Material:
    __name = ""
    __height = 0
    __length = 0
    __width = 0
    __barcode = 0

    __max_height_material = 200

    # TODO: temp choice height_warehouse
    def __init__(self, barcode: int, name: str, height: int, length: int, width: int, height_warehouse):

        # check height of a material
        if height > height_warehouse:
            raise ValueError("The height of element " +
                             name +
                             " is too high (max height: " +
                             str(self.__max_height_material) + ")")

        self.__barcode = barcode
        self.__name = name
        self.__height = height
        self.__length = length
        self.__width = width

    def get_barcode(self):
        return self.__barcode

    def get_name(self):
        return self.__name

    def get_height(self):
        return self.__height

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width
