from automatic_warehouse.status_warehouse.entry.entry import Entry


class EmptyEntry(Entry):
    """
    It is an entry of the warehouse where there is no tray.

    :type offset_x: int
    :type pos_y: int
    :param offset_x: offset x of the empty entry.
    :param pos_y: y of the empty entry.
    """
    
    def __init__(self, offset_x: int, pos_y: int):
        super().__init__(offset_x, pos_y)

    def __deepcopy__(self, memo):
        copy_obj = EmptyEntry(self.offset_x, self.pos_y)
        return copy_obj

    def __eq__(self, other):
        return (
            isinstance(other, EmptyEntry) and
            Entry.__eq__(self, other)
        )

    def __hash__(self):
        return 18341 ^ Entry.__hash__(self)
