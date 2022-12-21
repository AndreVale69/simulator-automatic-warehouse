class Entry:
    def __init__(self, offset_x: int, pos_y: int):
        self.offset_x = offset_x
        self.pos_y = pos_y

    def __deepcopy__(self, memo):
        copy_obj = type(self)(self.get_offset_x(), self.get_pos_y())
        copy_obj.offset_x = self.get_offset_x()
        copy_obj.pos_y = self.get_pos_y()
        return copy_obj

    def get_offset_x(self):
        return self.offset_x

    def get_pos_y(self):
        return self.pos_y
