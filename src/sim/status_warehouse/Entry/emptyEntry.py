from sim.status_warehouse.Entry.entry import Entry


class EmptyEntry(Entry):
    def __init__(self, offset_x: int, pos_y: int):
        super().__init__(offset_x, pos_y)

    def __deepcopy__(self, memo):
        copy_obj = EmptyEntry(self.get_offset_x(), self.get_pos_y())
        return copy_obj
