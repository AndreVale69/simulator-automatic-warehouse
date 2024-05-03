from abc import abstractmethod


class Entry:
    def __init__(self, offset_x: int, pos_y: int):
        """
        Superclass for all entries.

        :type offset_x: int
        :type pos_y: int
        :param offset_x: offset x of the entry.
        :param pos_y: position y of the entry.
        """
        self.offset_x = offset_x
        self.pos_y = pos_y

    def __eq__(self, other):
        return (
            isinstance(other, Entry) and
            self.get_offset_x() == other.get_offset_x() and
            self.get_pos_y() == other.get_pos_y()
        )

    def __hash__(self):
        return hash((self.offset_x, self.pos_y))

    @abstractmethod
    def __deepcopy__(self, memo):
        pass

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
