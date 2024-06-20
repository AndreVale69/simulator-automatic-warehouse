from logging import getLogger

from src.warehouse_configuration_singleton import WarehouseConfiguration, ColumnConfiguration

logger = getLogger(__name__)


class ConfigValidatorError(Exception):
    """ Exception raised when a configuration validation fails. """
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)


class ConfigurationValidator:
    def __init__(self, schema: WarehouseConfiguration):
        self._schema = schema

    def validate(self):
        schema = self._schema
        self._height_cols_less_than_warehouse(schema.columns, schema.height_warehouse)
        self._default_height_space_multiple_of_cols(schema.default_height_space, schema.columns)

    @staticmethod
    def _height_cols_less_than_warehouse(cols: list[ColumnConfiguration], height_warehouse: int) -> None:
        """
        Property to validate:
        The height property of each column can't be greater than the height of the warehouse (height_warehouse).

        :type cols: list[ColumnConfiguration]
        :type height_warehouse: int
        :param cols: columns.
        :param height_warehouse: height of the warehouse.
        :raises ConfigValidatorError: if the property is invalid.
        """
        for col in cols:
            if col.height > height_warehouse:
                raise ConfigValidatorError(
                    f"The height of the column with x_offset {col.x_offset} "
                    f"is greater than the height of the warehouse {height_warehouse}"
                )

    @staticmethod
    def _default_height_space_multiple_of_cols(default_height_space: int, cols: list[ColumnConfiguration]) -> None:
        """
        Properties to validate:
        1. The default_height_space should be a multiple of any column,
           otherwise the number of drawers in a column could be float (impossible).
        2. The height_last_position should be a multiple of default_height_space
           because it indicates how many entries are in the last position of the column.

        :type default_height_space: int
        :type cols: list[ColumnConfiguration]
        :param default_height_space: the default height space used in the warehouse.
        :param cols: columns.
        :raises ConfigValidatorError: if the property is invalid.
        """
        for col in cols:
            # check height_last_position is a multiple
            if col.height_last_position % default_height_space != 0:
                raise ConfigValidatorError(
                    f"The height of the last position of the column with x_offset {col.x_offset} "
                    f"is not a multiple of the default height space {default_height_space}"
                )

            # remove height_last_position from the height and check if it's a multiple
            if (col.height - col.height_last_position) % default_height_space != 0:
                raise ConfigValidatorError(
                    f"The height of the column with x_offset {col.x_offset} "
                    f"is not a multiple of the default height space {default_height_space}"
                )
