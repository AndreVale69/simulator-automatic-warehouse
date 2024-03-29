from abc import abstractmethod


class Entry:
    def __init__(self, offset_x: int, pos_y: int):
        self.offset_x = offset_x
        self.pos_y = pos_y

    def __eq__(self, other):
        return isinstance(other, Entry) and \
            self.get_offset_x() == other.get_offset_x() and \
            self.get_pos_y() == other.get_pos_y()

    @abstractmethod
    def __deepcopy__(self, memo):
        pass

    def get_offset_x(self):
        return self.offset_x

    def get_pos_y(self):
        return self.pos_y
