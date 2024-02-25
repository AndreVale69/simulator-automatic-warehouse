import os.path
from sim.status_warehouse.entry.drawer_entry import DrawerEntry
from sim.warehouse import Warehouse


def save_config(warehouse: Warehouse):
    """
    This function should only be used for debugging purposes.
    It saves the state to a file: <code>/tmp/config_warehouse.txt</code><br><br>
    @param warehouse: warehouse to save.
    """
    # if the directory doesn't exist, create it
    if not os.path.isdir("../../tmp"):
        os.mkdir("../../tmp")
    # create file
    with open("../../tmp/config_warehouse.txt", 'w') as file:
        # header
        file.write(f"Warehouse situation\n")
        file.write("\n")
        file.write("~" * 40 + "\n")
        file.write("\n")

        # carousel
        file.write(f"Number of drawers   : {warehouse.get_carousel().get_num_drawers()}\n")
        file.write(f"Number of spaces    : {warehouse.get_carousel().get_num_entries_free()}\n")
        file.write(f"Number of materials : {warehouse.get_carousel().get_num_materials()}\n")
        file.write("Carousel:\n")
        for entry in warehouse.get_carousel().get_container():
            file.write(f"[{entry}, {entry.get_drawer()}]\n" if type(entry) is DrawerEntry else f"[{entry}]\n")
        file.write("\n")
        file.write("~" * 40 + "\n")
        file.write("\n")

        # columns
        for column in warehouse.get_cols_container():
            file.write(f"Number of drawers   : {column.get_num_drawers()}\n")
            file.write(f"Number of spaces    : {column.get_num_entries_free()}\n")
            file.write(f"Number of materials : {column.get_num_materials()}\n")
            file.write(f"Offset x Column     : {column.get_offset_x()}\n")
            for entry in column.get_container():
                file.write(f"[{entry}, {entry.get_drawer()}]\n" if type(entry) is DrawerEntry else f"[{entry}]\n")
            file.write("\n")
            file.write("~" * 40 + "\n")
            file.write("\n")