from enum import Enum


class ActionEnum(Enum):
    EXTRACT_DRAWER = "ExtractDrawer"
    SEND_BACK_DRAWER = "SendBackDrawer"
    INSERT_RANDOM_MATERIAL = "InsertRandomMaterial"
    REMOVE_RANDOM_MATERIAL = "RemoveRandomMaterial"
