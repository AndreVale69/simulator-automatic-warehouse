import copy


class Entry:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __deepcopy__(self, memo):
        copy_obj = type(self)(self.get_pos_x(), self.get_pos_y())
        copy_obj.pos_x = self.get_pos_x()
        copy_obj.pos_y = self.get_pos_y()
        return copy_obj

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y
