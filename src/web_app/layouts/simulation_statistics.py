import dash_bootstrap_components as dbc
from typing import NamedTuple
from dash import html
from sim.utils.statistics.warehouse_statistics import WarehouseStatistics, TimeEnum


class SimulationInput(NamedTuple):
    num_actions: int
    drawers_to_gen: int
    materials_to_gen: int
    gen_deposit: bool
    gen_buffer: bool


def create_simulation_statistics_layout(
        warehouse_statistics: WarehouseStatistics,
        simulation_input: SimulationInput
) -> dbc.Card:
    return dbc.Card([
        _create_header(),
        _create_body(warehouse_statistics, simulation_input),
        _create_footer()
    ])


def _create_header() -> dbc.CardHeader | None:
    return dbc.CardHeader(children=html.H4("Simulation statistics", className="card-title"))


def _create_body(warehouse_statistics: WarehouseStatistics, simulation_input: SimulationInput) -> dbc.CardBody | None:
    input_title = html.H5("Input", className="card-text")
    input_body = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Description"), html.Th("Value")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td("Number of simulated actions requested"),
                html.Td(id="num_action_sim_stats", children=simulation_input.num_actions)
            ]),
            html.Tr([
                html.Td("Drawers requested to generate"),
                html.Td(id="drawers_to_gen_sim_stats", children=simulation_input.drawers_to_gen)
            ]),
            html.Tr([
                html.Td("Materials requested to generate"),
                html.Td(id="materials_to_gen_sim_stats", children=simulation_input.materials_to_gen)
            ]),
            html.Tr([
                html.Td("Deposit drawer generated"),
                html.Td(id="gen_deposit_sim_stats", children=str(simulation_input.gen_deposit))
            ]),
            html.Tr([
                html.Td("Buffer drawer generated"),
                html.Td(id="gen_buffer_sim_stats", children=str(simulation_input.gen_buffer))
            ])
        ])
    ], className="card-text")
    input_card = dbc.Card([dbc.CardHeader(input_title), dbc.CardBody(input_body)])

    process_time_title = html.H5("Process Time", className="card-text")
    total_simulation_time = warehouse_statistics.total_simulation_time()
    process_time_body = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Description"), html. Th("Value")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td("Start of the simulation"),
                html.Td(id="start_time_sim", children=warehouse_statistics.start_time_simulation().strftime('%a %d %b %Y, %H:%M:%S'))
            ]),
            html.Tr([
                html.Td("End of the simulation"),
                html.Td(id="finish_time_sim", children=warehouse_statistics.finish_time_simulation().strftime('%a %d %b %Y, %H:%M:%S'))
            ]),
            html.Tr([
                html.Td("Total simulation time"),
                html.Td(id="total_time_sim", children=f"{total_simulation_time.days} days, {str(total_simulation_time.components.hours).zfill(2)}:{str(total_simulation_time.components.minutes).zfill(2)}:{str(total_simulation_time.components.seconds).zfill(2)}")
            ])
        ])
    ], className="card-text")
    process_time_card = dbc.Card([dbc.CardHeader(process_time_title), dbc.CardBody(process_time_body)])

    output_title = html.H5("Output", className="card-text")
    output_body = dbc.Row([
        dbc.Col([dbc.Label("Number of actions started every hour"),
                 dbc.Table.from_dataframe(warehouse_statistics.actions_started_every(TimeEnum.HOUR))]),
        dbc.Col([dbc.Label("Number of actions finished every hour"),
                 dbc.Table.from_dataframe(warehouse_statistics.actions_finished_every(TimeEnum.HOUR))]),
        dbc.Col([dbc.Label("Number of actions completed every hour"),
                 dbc.Table.from_dataframe(warehouse_statistics.actions_completed_every(TimeEnum.HOUR))])
    ])
    output_card = dbc.Card([dbc.CardHeader(output_title), dbc.CardBody(output_body)])
    return dbc.CardBody([
        dbc.Row([
            dbc.Col([input_card]),
            dbc.Col([process_time_card])
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([output_card])
        ])
    ])


def _create_footer() -> dbc.CardFooter | None:
    return None
