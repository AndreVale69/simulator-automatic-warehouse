from src.status_warehouse.status import Status


class RightColumn(Status):
    def __init__(self, column: list):
        super().__init__(column)

    # override
    def add_drawer(self):
        print("add")

    # override
    def remove_drawer(self):
        print("remove")
