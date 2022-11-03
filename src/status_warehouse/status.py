from abc import ABC, abstractmethod
from src.status_warehouse.left_column import LeftColumn
from src.status_warehouse.right_column import RightColumn


class Status(ABC):
    def __init__(self, column: list):
        self.__column = column.copy()

    @abstractmethod
    def add_drawer(self):
        pass

    @abstractmethod
    def remove_drawer(self):
        pass
