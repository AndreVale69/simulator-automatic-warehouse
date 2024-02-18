import dash_bootstrap_components as dbc
from dash import html
from sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton

WAREHOUSE_CONFIG = WarehouseConfigurationSingleton.get_instance().get_configuration()
COLUMNS = WAREHOUSE_CONFIG['columns']


def create_columns_layout(num_col: int) -> list[dbc.ListGroupItem]:
    column, labels = COLUMNS[num_col], ["Width:", "Height:", "Offset:", "Height last position:"]
    values = [column['width'], column['height'], column['x_offset'], column['height_last_position']]
    return [
        dbc.ListGroupItem([
            dbc.Label(html.B(label)),
            dbc.Input(type="text", value=f"{value} cm", disabled=True)
        ])
        for (label, value) in zip(labels, values)
    ]