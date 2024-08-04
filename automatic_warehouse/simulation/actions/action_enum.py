from __future__ import annotations

from enum import Enum


class ActionEnum(Enum):
    """
    Enumerate of the possible actions.
    """
    
    EXTRACT_TRAY = "ExtractTray"
    """ Extract Tray action. """

    SEND_BACK_TRAY = "SendBackTray"
    """ Send Back Tray action. """

    INSERT_RANDOM_MATERIAL = "InsertRandomMaterial"
    """ Insert Random Material action. """

    REMOVE_RANDOM_MATERIAL = "RemoveRandomMaterial"
    """ Remove Random Material action. """

    def __str__(self):
        # override string method to avoid .value whenever you want to print
        return self.value if type(self) == ActionEnum else super().__str__()

    @staticmethod
    def from_str(action_str: str) -> Enum | None:
        """
        Static method from string.

        :type action_str: str
        :rtype: ActionEnum | None
        :param action_str: action as string.
        :return: the ``ActionEnum`` or ``None``.
        """
        if action_str == ActionEnum.EXTRACT_TRAY.value:
            return ActionEnum.EXTRACT_TRAY
        elif action_str == ActionEnum.SEND_BACK_TRAY.value:
            return ActionEnum.SEND_BACK_TRAY
        elif action_str == ActionEnum.INSERT_RANDOM_MATERIAL.value:
            return ActionEnum.INSERT_RANDOM_MATERIAL
        elif action_str == ActionEnum.REMOVE_RANDOM_MATERIAL.value:
            return ActionEnum.REMOVE_RANDOM_MATERIAL
        return None
