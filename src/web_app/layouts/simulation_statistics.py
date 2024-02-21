import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from typing import NamedTuple
from dash import html, dcc
from pandas import DataFrame

from sim.status_warehouse.Simulate_Events.action_enum import ActionEnum
from sim.utils.statistics.warehouse_statistics import WarehouseStatistics, TimeEnum


class SimulationInput(NamedTuple):
    num_actions: int
    drawers_to_gen: int
    materials_to_gen: int
    gen_deposit: bool
    gen_buffer: bool
    time: int | str


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
            ]),
            html.Tr([
                html.Td("Total time of the simulation"),
                html.Td(id="total_time_sim_stats", children=str(simulation_input.time))
            ])
        ])
    ], className="card-text")
    input_card = dbc.Card([dbc.CardHeader(input_title), dbc.CardBody(input_body)], color="light", outline=True)

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
                html.Td(id="start_time_sim",
                        children=warehouse_statistics.start_time_simulation().strftime('%a %d %b %Y, %H:%M:%S'))
            ]),
            html.Tr([
                html.Td("End of the simulation"),
                html.Td(id="finish_time_sim",
                        children=warehouse_statistics.finish_time_simulation().strftime('%a %d %b %Y, %H:%M:%S'))
            ]),
            html.Tr([
                html.Td("Total simulation time"),
                html.Td(id="total_time_sim", children=f"{total_simulation_time.days} days, "
                                                      f"{str(total_simulation_time.components.hours).zfill(2)}:"
                                                      f"{str(total_simulation_time.components.minutes).zfill(2)}:"
                                                      f"{str(total_simulation_time.components.seconds).zfill(2)}")
            ])
        ])
    ], className="card-text")
    process_time_card = dbc.Card([dbc.CardHeader(process_time_title), dbc.CardBody(process_time_body)], color="light", outline=True)

    output_title = html.H5("Output", className="card-text")
    actions_started_every_hour: DataFrame = warehouse_statistics.actions_started_every(TimeEnum.HOUR)
    actions_finished_every_hour: DataFrame = warehouse_statistics.actions_finished_every(TimeEnum.HOUR)
    actions_completed_every_hour: DataFrame = warehouse_statistics.actions_completed_every(TimeEnum.HOUR)
    output_body = dbc.Accordion([
        dbc.AccordionItem(title="Number of actions started every hour", children=[
            dbc.Row([
                dbc.DropdownMenu([
                    dbc.DropdownMenuItem("View statistics for all actions", header=True),
                    dbc.DropdownMenuItem("None", id="output_stats-actions_started-none"),
                    dbc.DropdownMenuItem("View statistics for a specific action", header=True),
                ] + [
                    dbc.DropdownMenuItem(action.value, id=f"output_stats-actions_started-{action.value}") for action in ActionEnum
                ], color="primary", label="Show data of the action: None")
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dbc.Accordion([
                        dbc.AccordionItem(dbc.Table.from_dataframe(actions_started_every_hour), title="Data Table")
                    ], start_collapsed=True)
                ),
                dbc.Col(
                    dcc.Graph(figure=go.Figure(data=[go.Scatter(x=actions_started_every_hour['Start'],
                                                                y=actions_started_every_hour['Count'])]))
                )
            ])
        ]),

        dbc.AccordionItem(title="Number of actions finished every hour", children=[
            dbc.Row([
                dbc.DropdownMenu([
                    dbc.DropdownMenuItem("View statistics for all actions", header=True),
                    dbc.DropdownMenuItem("None", id="output_stats-actions_finished-none"),
                    dbc.DropdownMenuItem("View statistics for a specific action", header=True),
                ] + [
                    dbc.DropdownMenuItem(action.value, id=f"output_stats-actions_finished-{action.value}") for action in ActionEnum
                ], color="primary", label="Show data of the action: None")
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dbc.Accordion([
                        dbc.AccordionItem(dbc.Table.from_dataframe(actions_finished_every_hour), title="Data Table")
                    ], start_collapsed=True)
                ),
                dbc.Col(
                    dcc.Graph(figure=go.Figure(data=[go.Scatter(x=actions_finished_every_hour['Finish'],
                                                                y=actions_finished_every_hour['Count'])]))
                )
            ])
        ]),

        dbc.AccordionItem(title="Number of actions completed every hour", children=[
            dbc.Row([
                dbc.DropdownMenu([
                    dbc.DropdownMenuItem("View statistics for all actions", header=True),
                    dbc.DropdownMenuItem("None", id="output_stats-actions_completed-none"),
                    dbc.DropdownMenuItem("View statistics for a specific action", header=True),
                ] + [
                    dbc.DropdownMenuItem(action.value,
                    id=f"output_stats-actions_completed-{action.value}") for action in ActionEnum
                ], color="primary", label="Show data of the action: None")
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dbc.Accordion([
                        dbc.AccordionItem(dbc.Table.from_dataframe(actions_completed_every_hour), title="Data Table")
                    ], start_collapsed=True)
                ),
                dbc.Col(
                    dcc.Graph(figure=go.Figure(data=[go.Scatter(
                        y=[f"{actions_completed_every_hour['Start'][i]} - "
                           f"{actions_completed_every_hour['Finish'][i]}"
                           for i in range(actions_completed_every_hour['Count'].size)],
                        x=actions_completed_every_hour['Count']
                    )]))
                )
            ])
        ])
    ], start_collapsed=True, always_open=True)

    output_card = dbc.Card([dbc.CardHeader(output_title), dbc.CardBody(output_body)], color="light", outline=True)

    return dbc.CardBody([
        dbc.Row([
            dbc.Col([input_card]), dbc.Col([process_time_card])
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([output_card])
        ])
    ])


def _create_footer() -> dbc.CardFooter | None:
    return None
