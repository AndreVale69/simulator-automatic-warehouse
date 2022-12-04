import copy


class Entry:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __deepcopy__(self, memo):
        newone = type(self)(self.get_pos_x(), self.get_pos_y())
        newone.__dict__.update(self.__dict__)
        self.pos_x = copy.deepcopy(self.get_pos_x(), memo)
        self.pos_y = copy.deepcopy(self.get_pos_y(), memo)
        return newone

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y
