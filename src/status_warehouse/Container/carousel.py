from src.status_warehouse.Container.drawerContainer import DrawerContainer


class Carousel(DrawerContainer):
    def __init__(self, height: int):
        super().__init__(height)
        print("prova")

    # override
    def add_drawer(self):
        print("add")

    # override
    def remove_drawer(self):
        print("remove")
