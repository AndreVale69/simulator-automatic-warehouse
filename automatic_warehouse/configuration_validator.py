from __future__ import annotations

from logging import getLogger

from automatic_warehouse.warehouse_configuration_singleton import (
    WarehouseConfiguration,
    ColumnConfiguration,
    CarouselConfiguration
)

logger = getLogger(__name__)


class ConfigValidatorError(Exception):
    """ Exception raised when a configuration validation fails. """
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)


class ConfigurationValidator:
    """
    A configuration validator used to validate a 
    :class:`WarehouseConfiguration <automatic_warehouse.warehouse_configuration_singleton.WarehouseConfiguration>` schema.

    :type schema: WarehouseConfiguration
    :param schema: schema to validate.
    """
    def __init__(self, schema: WarehouseConfiguration):
        self._schema = schema

    def validate(self):
        """
        Validates the configuration against the schema.

        The properties checked are:

            1. The height property of each column can't be greater than the height of the warehouse (``height_warehouse``).
            2. The ``default_height_space`` should be a multiple of the column, otherwise the number of drawers in a column could be float (impossible).
            3. The ``height_last_position`` should be a multiple of ``default_height_space`` because it indicates how many entries are in the last position of the column.
            4. If a column has the same x_offset as the carousel, then that column is above the carousel. This means that:

                a. The sum of the height of the column plus the height of the hole, buffer and bay of the carousel should be equal to or less than ``height_warehouse``.
                b. (not an error, but a warning) The length should be equal.

            5. The maximum height of the tray should be less than the height of each column/carousel.
            6. The height of the hole in the carousel should be greater than the maximum height of the tray.
            7. Two columns should have a distance greater than or equal to zero.
            8. The height of the buffer plus the height of the carousel bay must not exceed the height of the warehouse.

        :raises ConfigValidatorError: if validation fails.
        """
        schema = self._schema
        height_warehouse = schema.height_warehouse
        default_height_space = schema.default_height_space
        carousel = schema.carousel
        maximum_height = schema.tray.maximum_height
        for col in schema.columns:
            self._height_cols_less_than_warehouse(col, height_warehouse)
            self._default_height_space_multiple_of_cols(default_height_space, col)
            self._x_offset_col_equal_to_carousel(col, carousel, height_warehouse)
            self._maximum_height_limit_less_than_col_carousel_height(maximum_height, col)
        self._maximum_height_limit_less_than_col_carousel_height(maximum_height, carousel)
        self._hole_carousel_grater_maximum_height_tray(carousel.hole_height, maximum_height)
        self._distance_between_columns(schema.columns)
        self._buffer_bay_height_less_warehouse_height(carousel, height_warehouse)

    @staticmethod
    def _height_cols_less_than_warehouse(col: ColumnConfiguration, height_warehouse: int) -> None:
        """
        Property to validate:
        The height property of each column can't be greater than the height of the warehouse (height_warehouse).

        :type col: ColumnConfiguration
        :type height_warehouse: int
        :param col: column.
        :param height_warehouse: height of the warehouse.
        :raises ConfigValidatorError: if the property is invalid.
        """
        if col.height > height_warehouse:
            raise ConfigValidatorError(
                f"The height of the column with x_offset {col.x_offset} "
                f"is greater than the height of the warehouse {height_warehouse}"
            )

    @staticmethod
    def _default_height_space_multiple_of_cols(default_height_space: int, col: ColumnConfiguration) -> None:
        """
        Properties to validate:
        1. The default_height_space should be a multiple of the column,
           otherwise the number of drawers in a column could be float (impossible).
        2. The height_last_position should be a multiple of default_height_space
           because it indicates how many entries are in the last position of the column.

        :type default_height_space: int
        :type col: ColumnConfiguration
        :param default_height_space: the default height space used in the warehouse.
        :param col: column.
        :raises ConfigValidatorError: if the properties are invalid.
        """
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

    @staticmethod
    def _x_offset_col_equal_to_carousel(
            col: ColumnConfiguration, carousel: CarouselConfiguration, height_warehouse: int
    ) -> None:
        """
        Properties to validate:
        If a column has the same x_offset as the carousel, then that column is above the carousel.
        This means that:
        1. The sum of the height of the column plus the height of the hole,
           buffer and bay of the carousel should be equal to or less than height_warehouse.
        2. The length should be equal.
        The second property is only a warning.

        :param col: column.
        :param carousel: carousel.
        :param height_warehouse: height of the warehouse.
        :raises ConfigValidatorError: if the properties are invalid.
        """
        if col.x_offset != carousel.x_offset: return
        if col.height + carousel.hole_height + carousel.buffer_height + carousel.bay_height > height_warehouse:
            raise ConfigValidatorError(
                f"The height of the column with x_offset {col.x_offset}, plus the height of the carousel "
                f"(hole {carousel.hole_height} + buffer {carousel.buffer_height} + bay {carousel.bay_height}) "
                f"is grater than the height of the warehouse {height_warehouse}"
            )
        if col.length != carousel.length:
            logger.warning(f"The length of the column with x_offset {col.x_offset} "
                           f"is grater than the height of the carousel. Is it an error?")

    @staticmethod
    def _maximum_height_limit_less_than_col_carousel_height(maximum_height: int, container: ColumnConfiguration | CarouselConfiguration) -> None:
        """
        Properties to validate:
        The maximum height of the tray should be less than the height of each column/carousel.

        :type maximum_height: int
        :type container: ColumnConfiguration | CarouselConfiguration
        :param maximum_height: maximum height of the tray.
        :param container: column or carousel.
        :raises ConfigValidatorError: if the properties are invalid.
        """
        if isinstance(container, ColumnConfiguration):
            if maximum_height >= container.height:
                raise ConfigValidatorError(
                    f"The maximum height of the tray {maximum_height} is grater "
                    f"or equal to the height of the column {container.height}"
                )
        elif isinstance(container, CarouselConfiguration):
            if maximum_height >= container.buffer_height:
                raise ConfigValidatorError(
                    f"The maximum height of the tray {maximum_height} is grater "
                    f"or equal to the height of the buffer {container.buffer_height}"
                )
            elif maximum_height >= container.bay_height + container.hole_height:
                raise ConfigValidatorError(
                    f"The maximum height of the tray {maximum_height} is grater "
                    f"or equal to the height of the bay+hole {container.bay_height + container.hole_height}"
                )

    @staticmethod
    def _hole_carousel_grater_maximum_height_tray(hole_carousel: int, maximum_height_tray: int) -> None:
        """
        Property to validate:
        The height of the hole in the carousel should be greater than the maximum height of the tray.

        :param hole_carousel: height of the hole of the carousel.
        :param maximum_height_tray: maximum height of the tray.
        :raises ConfigValidatorError: if the property is invalid.
        """
        if hole_carousel <= maximum_height_tray:
            raise ConfigValidatorError(
                f"The hole carousel {hole_carousel} cannot be less or equal "
                f"than the maximum height of the tray {maximum_height_tray}."
            )

    @staticmethod
    def _distance_between_columns(cols: list[ColumnConfiguration]) -> None:
        """
        Property to validate:
        Two columns should have a distance greater than or equal to zero.

        :type cols: list[ColumnConfiguration]
        :param cols: columns.
        :raises ConfigValidatorError: if the property is invalid.
        """
        left = set()
        right = set()
        for col in cols:
            before_l = len(left)
            before_r = len(right)
            right.add((col.width // 2) - col.x_offset)
            left.add((col.width // 2) + col.x_offset)
            if len(right) == before_r or len(left) == before_l:
                raise ConfigValidatorError("Two columns have the distance less or equal to zero")

    @staticmethod
    def _buffer_bay_height_less_warehouse_height(carousel: CarouselConfiguration, height_warehouse: int):
        """
        Property to validate:
        The height of the buffer plus the height of the carousel bay must not exceed the height of the warehouse.

        :param carousel:
        :param height_warehouse:
        :return:
        """
        if carousel.buffer_height + carousel.bay_height >= height_warehouse:
            raise ConfigValidatorError(
                f"The height of the buffer {carousel.buffer_height} plus "
                f"the height of the carousel bay {carousel.bay_height} "
                f"must not exceed the height of the warehouse {height_warehouse}."
            )
