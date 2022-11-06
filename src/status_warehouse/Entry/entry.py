from abc import ABC, abstractmethod


class Entry(ABC):
    def __init__(self):
        print("Entry")
