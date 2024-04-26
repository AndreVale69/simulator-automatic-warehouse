from enum import Enum


class ActionEnum(Enum):
    """
    Enumerate of the possible actions.
    """
    EXTRACT_DRAWER = "ExtractDrawer"
    SEND_BACK_DRAWER = "SendBackDrawer"
    INSERT_RANDOM_MATERIAL = "InsertRandomMaterial"
    REMOVE_RANDOM_MATERIAL = "RemoveRandomMaterial"

    def __str__(self):
        # override string method to avoid .value whenever you want to print
        return self.value if type(self) == ActionEnum else super().__str__()

    @staticmethod
    def from_str(action_str: str):
        match action_str:
            case "ExtractDrawer":
                return ActionEnum.EXTRACT_DRAWER
            case "SendBackDrawer":
                return ActionEnum.SEND_BACK_DRAWER
            case "InsertRandomMaterial":
                return ActionEnum.INSERT_RANDOM_MATERIAL
            case "RemoveRandomMaterial":
                return ActionEnum.REMOVE_RANDOM_MATERIAL
            case _:
                return None
