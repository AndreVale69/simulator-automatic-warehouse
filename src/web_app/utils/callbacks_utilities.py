from typing import NamedTuple
from functools import lru_cache


class FieldsNewSimulation(NamedTuple):
    num_actions_sim: int | None
    num_drawers_sim: int | None
    num_materials_sim: int | None
    checkbox_time_sim: bool | None
    time_sim: str | None


@lru_cache
def fields_new_simulation_are_valid(fields: FieldsNewSimulation) -> bool:
    """
    1. Check if actions number is valid. <br>
    2. Check if drawers number is valid. <br>
    3. Check if materials number is valid. <br>
    4. Check if the time of the simulation has been triggered and if the time value is not None or 00:00.

    @param fields: use FieldsNewSimulation class.
    @return: True if the fields are valid, false otherwise
    """
    return True if (fields.num_actions_sim is not None and
                    fields.num_drawers_sim is not None and
                    fields.num_materials_sim is not None and
                    not (fields.checkbox_time_sim and (
                            fields.time_sim is None or fields.time_sim == "00:00:00"
                    ))) else False
