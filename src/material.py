# TODO: improve this class
class Material:
    __name = ""
    __height = 0
    __length = 0
    __width = 0
    __barcode = 0

    def __init__(self, barcode: int, name: str, height: int, length: int, width: int):
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
