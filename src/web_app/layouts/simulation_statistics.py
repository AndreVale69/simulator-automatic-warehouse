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
    html_sim_input_title = html.H5("Simulation Input", className="card-text")
    html_sim_input = html.Ul([
        html.Li(f"Number of simulated actions requested: {simulation_input.num_actions}"),
        html.Li(f"Drawers requested to generate: {simulation_input.drawers_to_gen}"),
        html.Li(f"Materials requested to generate: {simulation_input.materials_to_gen}"),
        html.Li(f"Deposit drawer generated: {simulation_input.gen_deposit}"),
        html.Li(f"Buffer drawer generated: {simulation_input.gen_buffer}")
    ], className="card-text")

    html_sim_time_title = html.H5("Simulation Time", className="card-text")
    html_sim_time = html.Ul([
        html.Li(f"Start of the simulation: {warehouse_statistics.start_time_simulation()}"),
        html.Li(f"End of the simulation: {warehouse_statistics.finish_time_simulation()}"),
        html.Li(f"Total simulation time: {warehouse_statistics.total_simulation_time()}")
    ], className="card-text")

    html_sim_output_title = html.H5("Simulation Output", className="card-text")
    html_sim_output = html.Ul([
        html.Li(["Number of actions started every hour:",
                 dbc.Table.from_dataframe(warehouse_statistics.actions_started_every(TimeEnum.HOUR))]),
        html.Li(["Number of actions finished every hour:",
                 dbc.Table.from_dataframe(warehouse_statistics.actions_finished_every(TimeEnum.HOUR))]),
        html.Li(["Number of actions completed every hour:",
                 dbc.Table.from_dataframe(warehouse_statistics.actions_completed_every(TimeEnum.HOUR))])
    ])
    return dbc.CardBody([
        dbc.Row([
            dbc.Col([html_sim_input_title, html_sim_input]),
            dbc.Col([html_sim_time_title, html_sim_time]),
            dbc.Col([html_sim_output_title, html_sim_output])
        ])
    ])


def _create_footer() -> dbc.CardFooter | None:
    return None
