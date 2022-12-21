from src.status_warehouse.Entry.entry import Entry


class EmptyEntry(Entry):
    def __init__(self, offset_x: int, pos_y: int):
        super().__init__(offset_x, pos_y)

    def __deepcopy__(self, memo):
        return super().__deepcopy__(memo)
