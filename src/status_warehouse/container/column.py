import copy
import random
from typing import NamedTuple

from src.tray import Tray
from src.material import gen_rand_materials
from src.status_warehouse.container.tray_container import TrayContainer
from src.status_warehouse.entry.tray_entry import TrayEntry
from src.status_warehouse.entry.empty_entry import EmptyEntry
from src.warehouse_configuration_singleton import ColumnConfiguration



class GenMaterialsAndTraysReturns(NamedTuple):
    """ Values returned by the gen_materials_and_trays method. """
    trays_inserted: int
    materials_inserted: int


class Column(TrayContainer):
    def __init__(self, info: ColumnConfiguration, warehouse):
        """
        The column is a simple column of the warehouse.
        It can't be where there is the bay and the buffer.
        It is thought to store the trays.

        :type info: ColumnConfiguration
        :type warehouse: Warehouse
        :param info: info about the column (config).
        :param warehouse: the warehouse where the column is located.
        """
        super().__init__(info.height, info.x_offset, info.width, warehouse)

        self.width = info.width
        self.height_last_position = info.height_last_position // self.get_def_space()

        # create container
        for i in range(self.get_num_entries()):
            self.create_new_space(EmptyEntry(info.x_offset, i))

    def __deepcopy__(self, memo):
        info = ColumnConfiguration(
            height =self.get_num_entries() * self.get_def_space(),
            x_offset = self.get_offset_x(),
            width = self.get_width(),
            height_last_position = self.get_height_last_position() * self.get_def_space()
        )
        copy_obj = Column(info, self.get_warehouse())
        copy_obj.container = copy.deepcopy(self.get_container(), memo)
        return copy_obj

    def __eq__(self, other):
        return (
            isinstance(other, Column) and
            TrayContainer.__eq__(self, other) and
            self.get_height_last_position() == other.get_height_last_position()
        )

    def __hash__(self):
        return (
            15199 ^
            TrayContainer.__hash__(self) ^
            hash(self.get_height_last_position())
        )

    def get_height_last_position(self) -> int:
        """
        Get the height of the last position.

        :rtype: int
        :return: the height of the last position.
        """
        return self.height_last_position

    def get_num_entries_free(self) -> int:
        count = entries_to_remove = 0
        container = self.get_container()
        height_last_position = self.get_height_last_position()

        # count the number of empty entries
        for entry in container:
            if isinstance(entry, EmptyEntry):
                count += 1

        # if the last position is not occupied, remove the clones
        if not self.last_position_is_occupied():
            return count - height_last_position + 1

        # otherwise, if it's occupied, remove the garbage entries
        for index in range(0, height_last_position):
            if isinstance(container[index], EmptyEntry):
                entries_to_remove += 1
        return count - entries_to_remove

    def last_position_is_occupied(self) -> bool:
        """
        Check if the last position is occupied.

        :rtype: bool
        :return: True if the last position is occupied, False otherwise.
        """
        return isinstance(self.container[self.height_last_position - 1], TrayEntry)

    def is_full(self) -> bool:
        return self.get_num_entries_free() == 0

    def is_empty(self) -> bool:
        return (self.get_num_entries() - self.height_last_position + 1) == self.get_num_entries_free()

    def add_tray(self, tray: Tray, index: int = 0):
        """
        Add a tray to the column.

        :type tray: Tray
        :type index: int
        :param tray: tray to be added.
        :param index: index of the column where to add the tray.
        """
        how_many = tray.get_num_space_occupied() + index - 1

        # Set as first trayEntry the lower limit.
        # For example, tray with 3 entries;
        # in the container the first trayEntry will be position 2,
        # and entries 0 and 1 are simple trayEntries.
        tray.set_first_trayEntry(self._create_trayEntry(tray, how_many))

        for index in range(index, how_many):
            self._create_trayEntry(tray, index)

    def _create_trayEntry(self, tray: Tray, index: int) -> TrayEntry:
        """
        Create a tray entry and add it to the column.

        :type tray: Tray
        :type index: int
        :rtype: TrayEntry
        :param tray: the tray to be added.
        :param index: where to add the tray.
        :return: the TrayEntry created.
        """
        # initialize positions
        tray_entry = TrayEntry(self.get_offset_x(), index)
        # connect Tray to Entry
        tray_entry.add_tray(tray)
        # add to container
        self.get_container()[index] = tray_entry
        # return the tray entry just added
        return tray_entry

    # override
    def remove_tray(self, tray: Tray) -> bool:
        """
        Remove a tray from the column.

        :type tray: Tray
        :rtype: bool
        :param tray: the tray to be removed.
        :return: True if the tray was removed, False otherwise.
        """
        entries_to_rmv: int = tray.get_num_space_occupied()
        container = self.get_container()
        for index, entry in enumerate(container):
            # if is a TrayEntry element
            # if the trays are the same (see __eq__ method)
            if isinstance(entry, TrayEntry) and entry.get_tray() == tray:
                container[index] = EmptyEntry(entry.get_offset_x(), entry.get_pos_y())
                entries_to_rmv -= 1
                if entries_to_rmv == 0:
                    return True

    def gen_materials_and_trays(self, num_trays: int, num_materials: int) -> GenMaterialsAndTraysReturns:
        """
        Generate random trays and materials.

        :type num_trays: int
        :type num_materials: int
        :rtype: GenMaterialsAndTraysReturns
        :param num_trays: number of trays to create in the warehouse
        :param num_materials: number of materials to create in the trays
        :return: a NamedTuple where we can find the trays_inserted and the materials_inserted
        """
        from src.utils.decide_position_algorithm.algorithm import decide_position
        from src.utils.decide_position_algorithm.enum_algorithm import Algorithm

        trays_to_insert = num_trays
        trays_inserted = 0
        materials_inserted = 0
        # generate (num_trays) trays
        for _ in range(trays_to_insert):
            # check if there is space in the column
            if self.is_full():
                break

            # check if there are materials to generate
            num_materials_to_put = random.randint(1, num_materials) if num_materials > 0 else 0

            # create a tray
            tray_to_insert = Tray(gen_rand_materials(num_materials_to_put))
            # looking for the index where put the tray
            try:
                decide_position_res = decide_position(
                    columns=[self],
                    space_req=tray_to_insert.get_num_space_occupied(),
                    algorithm=Algorithm.HIGH_POSITION
                )
            except ValueError:
                continue
            # insert the tray
            self.add_tray(tray_to_insert, decide_position_res.index)
            # update local counter
            num_materials -= num_materials_to_put
            materials_inserted += num_materials_to_put
            trays_inserted += 1

        return GenMaterialsAndTraysReturns(trays_inserted, materials_inserted)
