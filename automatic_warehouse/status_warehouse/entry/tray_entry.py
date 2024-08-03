import copy

from automatic_warehouse.status_warehouse.entry.entry import Entry
from automatic_warehouse.status_warehouse.tray import Tray


class TrayEntry(Entry):
    """
    It is an entry of the warehouse where the tray is located.

    :type offset_x: int
    :type pos_y: int
    :param offset_x: offset x of the tray entry.
    :param pos_y: y of the tray entry.
    """

    def __init__(self, offset_x: int, pos_y: int):
        super().__init__(offset_x, pos_y)
        self.tray = None

    def __deepcopy__(self, memo):
        copy_obj = TrayEntry(self.offset_x, self.pos_y)
        copy_obj.tray = copy.deepcopy(self.tray, memo)
        if copy_obj == self.tray.get_first_tray_entry():
            copy_obj.tray.set_first_tray_entry(copy_obj)
        return copy_obj

    def __eq__(self, other):
        return (
            isinstance(other, TrayEntry) and
            Entry.__eq__(self, other)
        )

    def __hash__(self):
        return 17581 ^ Entry.__hash__(self) ^ hash(self.tray)

    def get_tray(self) -> Tray:
        """
        Get the pointer to the tray to which the ``TrayEntry`` belongs.

        :rtype: Tray
        :return: the Tray pointer.
        """
        return self.tray

    def add_tray(self, tray: Tray):
        """
        Add the tray pointer to the local reference.

        :type tray: Tray
        :param tray: tray pointer.
        """
        # copy "pointer"
        self.tray = tray
