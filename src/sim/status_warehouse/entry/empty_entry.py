from src.sim.status_warehouse.entry.entry import Entry


class EmptyEntry(Entry):
    def __init__(self, offset_x: int, pos_y: int):
        """
        It is an entry of the warehouse where there is no drawer.

        :type offset_x: int
        :type pos_y: int
        :param offset_x: offset x of the empty entry.
        :param pos_y: y of the empty entry.
        """
        super().__init__(offset_x, pos_y)

    def __deepcopy__(self, memo):
        copy_obj = EmptyEntry(self.get_offset_x(), self.get_pos_y())
        return copy_obj
