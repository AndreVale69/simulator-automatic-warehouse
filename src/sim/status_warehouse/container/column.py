import copy
import random
from typing import NamedTuple

from src.sim.drawer import Drawer
from src.sim.material import gen_rand_materials
from src.sim.status_warehouse.container.drawer_container import DrawerContainer
from src.sim.status_warehouse.entry.drawer_entry import DrawerEntry
from src.sim.status_warehouse.entry.empty_entry import EmptyEntry


class GenMaterialsAndDrawersReturns(NamedTuple):
    """ Values returned by the gen_materials_and_drawers method. """
    drawers_inserted: int
    materials_inserted: int


class Column(DrawerContainer):
    def __init__(self, info: dict, warehouse):
        """
        The column is a simple column of the warehouse.
        It can't be where there is the bay and the buffer.
        It is thought to store the drawers.

        :type info: dict
        :type warehouse: Warehouse
        :param info: info about the column (config).
        :param warehouse: the warehouse where the column is located.
        """
        super().__init__(info["height"], info["x_offset"], info["width"], warehouse)

        self.width = info["width"]
        self.height_last_position = info["height_last_position"] // self.get_def_space()

        # create container
        for i in range(self.get_height_container()):
            self.create_new_space(EmptyEntry(info["x_offset"], i))

    def __deepcopy__(self, memo):
        info: dict = {
            "height": self.get_height_container() * self.get_def_space(),
            "x_offset": self.get_offset_x(),
            "width": self.get_width(),
            "height_last_position": self.get_height_last_position() * self.get_def_space()
        }
        copy_obj = Column(info, self.get_warehouse())
        copy_obj.container = copy.deepcopy(self.get_container(), memo)
        return copy_obj

    def __eq__(self, other):
        return (
            isinstance(other, Column) and
            self.get_height_last_position() == other.get_height_last_position() and
            DrawerContainer.__eq__(self, other)
        )

    def __hash__(self):
        return (
            13 ^
            hash(self.get_height_last_position()) ^
            DrawerContainer.__hash__(self)
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
        return isinstance(self.container[self.height_last_position - 1], DrawerEntry)

    def is_full(self) -> bool:
        return self.get_num_entries_free() == 0

    def is_empty(self) -> bool:
        return (self.get_height_container() - self.height_last_position + 1) == self.get_num_entries_free()

    def add_drawer(self, drawer: Drawer, index: int = 0):
        """
        Add a drawer to the column.

        :type drawer: Drawer
        :type index: int
        :param drawer: drawer to be added.
        :param index: index of the column where to add the drawer.
        """
        how_many = drawer.get_num_space_occupied() + index - 1

        # Set as first drawerEntry the lower limit.
        # For example, drawer with 3 entries;
        # in the container the first drawerEntry will be position 2,
        # and entries 0 and 1 are simple drawerEntries.
        drawer.set_first_drawerEntry(self._create_drawerEntry(drawer, how_many))

        for index in range(index, how_many):
            self._create_drawerEntry(drawer, index)

    def _create_drawerEntry(self, drawer: Drawer, index: int) -> DrawerEntry:
        """
        Create a drawer entry and add it to the column.

        :type drawer: Drawer
        :type index: int
        :rtype: DrawerEntry
        :param drawer: the drawer to be added.
        :param index: where to add the drawer.
        :return: the DrawerEntry created.
        """
        # initialize positions
        drawer_entry = DrawerEntry(self.get_offset_x(), index)
        # connect Drawer to Entry
        drawer_entry.add_drawer(drawer)
        # add to container
        self.get_container()[index] = drawer_entry
        # return the drawer entry just added
        return drawer_entry

    # override
    def remove_drawer(self, drawer: Drawer) -> bool:
        """
        Remove a drawer from the column.

        :type drawer: Drawer
        :rtype: bool
        :param drawer: the drawer to be removed.
        :return: True if the drawer was removed, False otherwise.
        """
        entries_to_rmv: int = drawer.get_num_space_occupied()
        container = self.get_container()
        for index, entry in enumerate(container):
            # if is a DrawerEntry element
            # if the drawers are the same (see __eq__ method)
            if isinstance(entry, DrawerEntry) and entry.get_drawer() == drawer:
                container[index] = EmptyEntry(entry.get_offset_x(), entry.get_pos_y())
                entries_to_rmv -= 1
                if entries_to_rmv == 0:
                    return True

    def gen_materials_and_drawers(self, num_drawers: int, num_materials: int) -> GenMaterialsAndDrawersReturns:
        """
        Generate random drawers and materials.

        :type num_drawers: int
        :type num_materials: int
        :rtype: GenMaterialsAndDrawersReturns
        :param num_drawers: number of drawers to create in the warehouse
        :param num_materials: number of materials to create in the drawers
        :return: a NamedTuple where we can find the drawers_inserted and the materials_inserted
        """
        from src.sim.utils.decide_position_algorithm.algorithm import decide_position
        from src.sim.utils.decide_position_algorithm.enum_algorithm import Algorithm

        drawers_to_insert = num_drawers
        drawers_inserted = 0
        materials_inserted = 0
        # generate (num_drawers) drawers
        for _ in range(drawers_to_insert):
            # check if there is space in the column
            if self.is_full():
                break

            # check if there are materials to generate
            num_materials_to_put = random.randint(1, num_materials) if num_materials > 0 else 0

            # create a drawer
            drawer_to_insert = Drawer(gen_rand_materials(num_materials_to_put))
            # looking for the index where put the drawer
            try:
                decide_position_res = decide_position(
                    columns=[self],
                    space_req=drawer_to_insert.get_num_space_occupied(),
                    algorithm=Algorithm.HIGH_POSITION
                )
            except ValueError:
                continue
            # insert the drawer
            self.add_drawer(drawer_to_insert, decide_position_res.index)
            # update local counter
            num_materials -= num_materials_to_put
            materials_inserted += num_materials_to_put
            drawers_inserted += 1

        return GenMaterialsAndDrawersReturns(drawers_inserted, materials_inserted)
