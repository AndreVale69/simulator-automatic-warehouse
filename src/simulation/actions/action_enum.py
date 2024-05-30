from enum import Enum


class ActionEnum(Enum):
    """
    Enumerate of the possible actions.
    """
    EXTRACT_TRAY = "ExtractTray"
    SEND_BACK_TRAY = "SendBackTray"
    INSERT_RANDOM_MATERIAL = "InsertRandomMaterial"
    REMOVE_RANDOM_MATERIAL = "RemoveRandomMaterial"

    def __str__(self):
        # override string method to avoid .value whenever you want to print
        return self.value if type(self) == ActionEnum else super().__str__()

    @staticmethod
    def from_str(action_str: str) -> Enum | None:
        """
        Static method from string.

        :type action_str: str
        :rtype ActionEnum | None
        :param action_str: action as string
        :return: the ActionEnum or None
        """
        match action_str:
            case ActionEnum.EXTRACT_TRAY.value:
                return ActionEnum.EXTRACT_TRAY
            case ActionEnum.SEND_BACK_TRAY.value:
                return ActionEnum.SEND_BACK_TRAY
            case ActionEnum.INSERT_RANDOM_MATERIAL.value:
                return ActionEnum.INSERT_RANDOM_MATERIAL
            case ActionEnum.REMOVE_RANDOM_MATERIAL.value:
                return ActionEnum.REMOVE_RANDOM_MATERIAL
            case _:
                return None
