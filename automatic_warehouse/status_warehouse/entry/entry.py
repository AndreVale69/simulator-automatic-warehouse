class Entry:
    """
    Superclass for all entries.

    :type offset_x: int
    :type pos_y: int
    :param offset_x: offset x of the entry.
    :param pos_y: position y of the entry.
    """

    def __init__(self, offset_x: int, pos_y: int):
        self.offset_x = offset_x
        self.pos_y = pos_y

    def __eq__(self, other):
        return (
            isinstance(other, Entry) and
            self.offset_x == other.offset_x and
            self.pos_y == other.pos_y
        )

    def __hash__(self):
        return 11497 ^ hash((self.offset_x, self.pos_y))

    def get_offset_x(self) -> int:
        """
        Get the offset x value of the entry.

        :rtype: int
        :return: the offset x value of the entry.
        """
        return self.offset_x

    def get_pos_y(self) -> int:
        """
        Get the position y value of the entry.

        :rtype: int
        :return: the position y value of the entry.
        """
        return self.pos_y
