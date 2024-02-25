# Run this app with `python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os.path
import shutil
import sys
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash_auth import BasicAuth

from signal import signal, SIGINT, SIGTERM
from diskcache import Cache
from dash import Dash, dcc, html, Input, Output, ctx, State, DiskcacheManager
from datetime import datetime
from dash.exceptions import PreventUpdate
from pandas import DataFrame

from src.sim.warehouse import Warehouse
from web_app.components.timeline import Timeline
from web_app.components.navbar import navbar
from src.web_app.configuration import HOST, PORT, PROXY
from pages import documentation, not_found_404
from sim.warehouse_configuration_singleton import WarehouseConfigurationSingleton
from web_app.layouts.custom_configuration import create_columns_layout
from sim.utils.statistics.warehouse_statistics import WarehouseStatistics, TimeEnum
from sim.utils.statistics.warehouse_statistics import ActionEnum
from web_app.layouts.simulation_statistics import SimulationInput, create_simulation_statistics_layout
from web_app.utils.callbacks_utilities import FieldsNewSimulationArgs, fields_new_simulation_are_valid


"""
    #####################
    * Set-up simulation *
    #####################
"""

# Initialize the Warehouse for simulation
warehouse = Warehouse()
warehouse.run_simulation()
warehouse_config = WarehouseConfigurationSingleton.get_instance().get_configuration()
warehouse_statistics = WarehouseStatistics(DataFrame(warehouse.get_simulation().get_store_history().items))


"""
    #########################
    * Set-up all components *
    #########################
"""
# documentation: https://dash.plotly.com/background-callbacks
cache = Cache("./cache")
# create the path if it doesn't exist.
# this path will be used by the application to create downloadable graphics
if not os.path.isdir('./images'):
    os.mkdir('./images')

# Import bootstrap components
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
app = Dash(external_stylesheets=[BS, dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           # this ensures that mobile devices don't rescale your content on small screens
           # and lets you build mobile optimised layouts
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
           background_callback_manager=DiskcacheManager(cache), name=__name__)
# Very ridiculous security, but it's efficient against foolish users ;)
USER_PWD = {
    "admin": "admin"
}
BasicAuth(app, USER_PWD)

# timeline manager
timeline = Timeline(warehouse.get_simulation().get_store_history().items)

""" 
    ########################
    * Application's layout * 
    ########################
"""


# if you don't want to save the state between reloads of the page,
# see live updates on: https://dash.plotly.com/live-updates#updates-on-page-load
def index_layout():
 return html.Div(children=[
        navbar,
        html.Br(),
        dbc.Row([
            html.H1(
                children='Simulator Automatic Warehouse',
                style={'textAlign': 'center'}
            )
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(children=html.H4("New Simulation", className="card-title")),

                    dbc.CardBody([
                        dbc.ListGroup([
                            dbc.ListGroupItem([
                                dbc.Label('Total number of actions:'),
                                dbc.Input(id='num_actions_sim', type='number', min=1, step=1, placeholder='# Actions',
                                          required=True)
                                # TODO: add '?' and write in what does it means. You can use also 'info' icon (boostrap)
                            ]),
                            dbc.ListGroupItem([
                                dbc.Label('Total number of drawers:'),
                                dbc.Input(id='num_drawers_sim', type='number', min=1, step=1, placeholder='# Drawers')
                                # TODO: add check to avoid the number of drawers
                                #       being greater than the height of the warehouse.
                            ]),
                            dbc.ListGroupItem([
                                dbc.Label('Total number of materials:'),
                                dbc.Input(id='num_materials_sim', type='number', min=1, step=1,
                                          placeholder='# Materials')
                            ]),
                            dbc.ListGroupItem([
                                dbc.Label('Do you want fill carousel?'),
                                dbc.Checklist(
                                    options=[
                                        {"value": "gen_deposit", "label": "Generate deposit drawer"},
                                        {"value": "gen_buffer", "label": "Generate buffer drawer"},
                                    ],
                                    id="checklist_generators",
                                )
                            ]),
                            dbc.ListGroupItem([
                                dbc.Label('Total time of the simulation:'),
                                dbc.InputGroup([
                                    dbc.InputGroupText(dbc.Checkbox(id='checkbox_time_sim', value=False)),
                                    # dbc.Input(id='time_sim', type='number', min=1, step=1, placeholder='Seconds',
                                    #           readonly=True),
                                    dbc.Input(id='time_sim', type='time', min="00:00:01", max="23:59:59", step=1,
                                              readonly=True),
                                ]),
                            ])
                        ])
                    ]),

                    dbc.CardFooter([
                        dbc.Col([
                            dbc.Button(children='Run new simulation!', id='btn_new_simulation', n_clicks=0)
                        ], width={'offset': 2})
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(children=html.H4("Timeline of the simulation", className="card-title")),

                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col([
                                    dbc.Col([
                                        dbc.InputGroup([
                                            # info text
                                            dbc.InputGroupText(children='View range:'),
                                            # input text
                                            dbc.Input(id='set_step_graph', type='number', min=1,
                                                      value=timeline.get_step(),
                                                      max=timeline.get_tot_tabs(), step=1),
                                            dbc.InputGroupText(children='min.')
                                        ])
                                    ])
                                ], width='auto'),
                                dbc.Col([
                                    dbc.InputGroup([
                                        # go to extreme left
                                        dbc.Button([html.I(className='bi bi-chevron-bar-left')], id='btn_left_end',
                                                   n_clicks=0),
                                        # go to left
                                        dbc.Button([html.I(className='bi bi-chevron-left')], id='btn_left',
                                                   n_clicks=0),
                                        # text
                                        dbc.Input(id='actual_tab', type='number', min=1, max=timeline.get_tot_tabs(),
                                                  step=1,
                                                  value=timeline.get_actual_tab()),
                                        dbc.InputGroupText(id='num_tabs_graph', children=f'/{timeline.get_tot_tabs()}'),
                                        # go to right
                                        dbc.Button([html.I(className='bi bi-chevron-right')], id='btn_right',
                                                   n_clicks=0),
                                        # go to extreme right
                                        dbc.Button([html.I(className='bi bi-chevron-bar-right')], id='btn_right_end',
                                                   n_clicks=0)
                                    ])
                                ], width={"size": 'auto', "offset": 2}),
                                dbc.Col([
                                    # summary
                                    dbc.Button([html.I(className='bi bi-x-circle-fill'), " SUMMARY"], id='btn_summary',
                                               n_clicks=0)
                                ], width=2)
                            ]),
                            dbc.Row([dbc.FormText(id='set_step_graph_max_value_hint',
                                                  children=f'Max value: {timeline.get_tot_tabs()} min.')]),
                            dbc.Row([
                                dcc.Loading(
                                    children=[dcc.Graph(
                                        id='graph-actions',
                                        figure=timeline.get_figure()
                                    )],
                                    type="dot",
                                    parent_className="loading_wrapper"
                                )
                            ])
                        ]
                    ),

                    dbc.CardFooter(children=[
                        dbc.Row([
                            dbc.Col([
                                dbc.DropdownMenu(children=[
                                    dbc.DropdownMenuItem(
                                        children=[html.I(className='bi bi-download'), " EXCEL"],
                                        id="dropdown-btn_xlsx",
                                        n_clicks=0
                                    ),
                                    dbc.DropdownMenuItem(
                                        children=[html.I(className='bi bi-download'), " CSV"],
                                        id = "dropdown-btn_csv",
                                        n_clicks=0
                                    ),
                                    dbc.DropdownMenuItem(
                                        children=[html.I(className='bi bi-download'), " SVG"],
                                        id="dropdown-btn_svg",
                                        n_clicks=0
                                    ),
                                    dbc.DropdownMenuItem(
                                        children=[html.I(className='bi bi-download'), " PDF"],
                                        id="dropdown-btn_pdf",
                                        n_clicks=0
                                    )],
                                    label="Download Graph"
                                )
                            ], width=1)
                        ]),
                    ]),
                ])
            ], width=10)
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(children=html.H4("Current configuration", className="card-title")),

                    dbc.CardBody([
                        dbc.Accordion([
                            dbc.AccordionItem([
                                dbc.ListGroup([
                                    dbc.ListGroupItem([
                                        dbc.Label(html.B("Height warehouse:")),
                                        dbc.Input(type="text", value=f"{warehouse_config['height_warehouse']} cm", disabled=True)
                                    ]),
                                    dbc.ListGroupItem([
                                        dbc.Label(html.B("Speed per second:")),
                                        dbc.Input(type="text", value=f"{warehouse_config['speed_per_sec']} cm", disabled=True)
                                    ])
                                ])
                            ], title="General information"),
                            dbc.AccordionItem([
                                dbc.Select([
                                    f"Column {i + 1}" for i in range(len(warehouse_config['columns']))
                                ], "Column 1", id="config-choose_col"),
                                html.Br(),
                                dbc.ListGroup(
                                    # show column 0 as default
                                    create_columns_layout(0),
                                    id="config-show_col"
                                )
                            ], title="Columns"),
                            dbc.AccordionItem([
                                dbc.ListGroup([
                                    dbc.ListGroupItem([
                                        dbc.Label(html.B("Width:")),
                                        dbc.Input(type="text", value=f"{warehouse_config['carousel']['width']} cm", disabled=True)
                                    ]),
                                    dbc.ListGroupItem([
                                        dbc.Label(html.B("Hole height:")),
                                        dbc.Input(type="text", value=f"{warehouse_config['carousel']['hole_height']} cm", disabled=True)
                                    ]),
                                    dbc.ListGroupItem([
                                        dbc.Label(html.B("Deposit height:")),
                                        dbc.Input(type="text", value=f"{warehouse_config['carousel']['deposit_height']} cm", disabled=True)
                                    ]),
                                    dbc.ListGroupItem([
                                        dbc.Label(html.B("Buffer height:")),
                                        dbc.Input(type="text", value=f"{warehouse_config['carousel']['buffer_height']} cm", disabled=True)
                                    ]),
                                    dbc.ListGroupItem([
                                        dbc.Label(html.B("Bay height:")),
                                        dbc.Input(type="text", value=f"{warehouse_config['carousel']['deposit_height'] + warehouse_config['carousel']['buffer_height']} cm", disabled=True)
                                    ]),
                                    dbc.ListGroupItem([
                                        dbc.Label(html.B("Offset:")),
                                        dbc.Input(type="text", value=f"{warehouse_config['carousel']['x_offset']} cm", disabled=True)
                                    ]),
                                ])
                            ], title="Carousel")
                        ], start_collapsed=True, always_open=True)
                    ])
                ])
            ],
                width=2),
            dbc.Col([
                # TODO: download the statistics (?)
                create_simulation_statistics_layout(
                    warehouse_statistics,
                    SimulationInput(
                        warehouse_config['simulation']['num_actions'],
                        warehouse_config['simulation']['drawers_to_gen'],
                        warehouse_config['simulation']['materials_to_gen'],
                        warehouse_config['simulation']['gen_deposit'],
                        warehouse_config['simulation']['gen_buffer'],
                        warehouse_config['simulation'].get('time', 'Not specified')
                    )
                )
            ], width=10)
        ], justify="end"),
        dcc.Download(id="download-graph"),
        dcc.Download(id="download-stats"),
        dbc.Toast(
            "",
            id="toast_new_simulation_completed",
            header="Simulation completed!",
            is_open=False,
            dismissable=True,
            icon="success",
            style={"position": "fixed", "top": 10, "right": 10, "width": 350},
        ),
        dbc.Toast(
            "Error message.",
            id="toast_error_simulation",
            header="Error during simulation!",
            is_open=False,
            dismissable=True,
            icon="danger",
            style={"position": "fixed", "top": 10, "right": 10, "width": 350},
        ),
    ])

app_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.layout = app_layout

app.validation_layout = html.Div([
    app_layout,
    index_layout(),
    documentation.layout,
    not_found_404.layout
])

""" 
    ##########################
    * Application's callback * 
    ##########################
"""


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    match pathname:
        case '/':
            return index_layout()
        case '/index':
            return index_layout()
        case '/documentation':
            return documentation.layout
        case _:
            return not_found_404.layout


@app.callback(
    Output("btn_new_simulation", "disabled", allow_duplicate=True),
    Output("btn_new_simulation", "children", allow_duplicate=True),
    Input("btn_new_simulation", "n_clicks"),
    State('num_actions_sim', 'value'),
    State('num_drawers_sim', 'value'),
    State('num_materials_sim', 'value'),
    State('checkbox_time_sim', 'value'),
    State('time_sim', 'value'),
    prevent_initial_call=True
)
@cache.memoize()
def load_loading_button(n,
                        num_actions_sim,
                        num_drawers_sim,
                        num_materials_sim,
                        checkbox_time_sim,
                        time_sim):
    if fields_new_simulation_are_valid(
            FieldsNewSimulationArgs(num_actions_sim, num_drawers_sim, num_materials_sim, checkbox_time_sim, time_sim)
    ):
        return True, [dbc.Spinner(size="sm"), " Loading..."]

    raise PreventUpdate


@app.callback(
    Output("btn_new_simulation", "disabled", allow_duplicate=True),
    Output("btn_new_simulation", "children", allow_duplicate=True),
    Input("graph-actions", "figure"),
    prevent_initial_call=True
)
@cache.memoize()
def restore_btn_simulation(n):
    return False, "Run new simulation!"


@app.callback(
    Output("download-graph", "data"),
    Input("dropdown-btn_svg", "n_clicks"),
    Input("dropdown-btn_pdf", "n_clicks"),
    Input("dropdown-btn_csv", "n_clicks"),
    Input("dropdown-btn_xlsx", "n_clicks"),
    prevent_initial_call=True
)
def download_graph(b_svg, b_pdf, b_csv, b_xlsx):
    extension = ''
    # which button is triggered?
    match ctx.triggered_id:
        case "dropdown-btn_csv":
            timeline.get_dataframe().to_csv("./images/graph_actions.csv")
            return dcc.send_file("./images/graph_actions.csv")
        case "dropdown-btn_xlsx":
            timeline.get_dataframe().to_excel("./images/graph_actions.xlsx")
            return dcc.send_file("./images/graph_actions.xlsx")
        case "dropdown-btn_svg":
            extension = 'svg'
        case "dropdown-btn_pdf":
            extension = 'pdf'
        case _:
            raise PreventUpdate
    # create the file
    with open(f"./images/graph_actions.{extension}", "w"):
        pass
    # take graph to download
    timeline.get_figure().write_image(f"./images/graph_actions.{extension}", engine='kaleido', width=1920, height=1080)
    return dcc.send_file(
        f"./images/graph_actions.{extension}"
    )


# if you want to duplicate callback outputs https://dash.plotly.com/duplicate-callback-outputs
@app.callback(
    Output('graph-actions', 'figure'),
    Output('actual_tab', 'value'),
    Output('actual_tab', 'max'),
    Output('num_tabs_graph', 'children'),
    Output('set_step_graph_max_value_hint', 'children'),
    Output('set_step_graph', 'value'),
    Output('set_step_graph', 'max'),
    Output("toast_new_simulation_completed", "is_open"),
    Output("toast_new_simulation_completed", "children"),
    Output("toast_error_simulation", "is_open"),
    Output("toast_error_simulation", "children"),
    Output('start_time_sim', 'children'),
    Output('finish_time_sim', 'children'),
    Output('total_time_sim', 'children'),

    # output stats
    Output('output_stats-actions_started', 'label'),
    Output('output_stats-actions_started-data_table', 'children'),
    Output('output_stats-actions_started-figure', 'figure'),
    Output('output_stats-actions_finished', 'label'),
    Output('output_stats-actions_finished-data_table', 'children'),
    Output('output_stats-actions_finished-figure', 'figure'),
    Output('output_stats-actions_completed', 'label'),
    Output('output_stats-actions_completed-data_table', 'children'),
    Output('output_stats-actions_completed-figure', 'figure'),


    Input('btn_right', 'n_clicks'),
    Input('btn_left', 'n_clicks'),
    Input('btn_right_end', 'n_clicks'),
    Input('btn_left_end', 'n_clicks'),
    Input('btn_summary', 'n_clicks'),

    Input('actual_tab', 'value'),
    Input('set_step_graph', 'value'),

    # trigger new simulation button
    Input('btn_new_simulation', 'n_clicks'),

    State('num_actions_sim', 'value'),
    State('num_drawers_sim', 'value'),
    State('num_materials_sim', 'value'),
    State('checklist_generators', 'value'),
    State('checkbox_time_sim', 'value'),
    State('time_sim', 'value'),
    State('graph-actions', 'figure'),
    State('set_step_graph_max_value_hint', 'children'),
    State('set_step_graph', 'max'),
    State('actual_tab', 'max'),
    State('start_time_sim', 'children'),
    State('finish_time_sim', 'children'),
    State('total_time_sim', 'children'),
    State('output_stats-actions_started', 'label'),
    State('output_stats-actions_started-data_table', 'children'),
    State('output_stats-actions_started-figure', 'figure'),
    State('output_stats-actions_finished', 'label'),
    State('output_stats-actions_finished-data_table', 'children'),
    State('output_stats-actions_finished-figure', 'figure'),
    State('output_stats-actions_completed', 'label'),
    State('output_stats-actions_completed-data_table', 'children'),
    State('output_stats-actions_completed-figure', 'figure'),
    prevent_initial_call=True
)
@cache.memoize()
def update_timeline_components(val_btn_right, val_btn_left, val_btn_right_end, val_btn_left_end, val_btn_summary,
                               val_actual_tab, val_set_step_graph,
                               # trigger new simulation button
                               clicks_btn,
                               num_actions_sim, num_drawers_sim, num_materials_sim,
                               checklist_generators, checkbox_time_sim,
                               time_sim,
                               timeline_old,
                               set_step_graph_max_value_hint,
                               set_step_graph_max,
                               actual_tab_max,
                               start_time_sim, finish_time_sim, total_time_sim,
                               output_stats_actions_started,
                               output_stats_actions_started_data_table,
                               output_stats_actions_started_figure,
                               output_stats_actions_finished,
                               output_stats_actions_finished_data_table,
                               output_stats_actions_finished_figure,
                               output_stats_actions_completed,
                               output_stats_actions_completed_data_table,
                               output_stats_actions_completed_figure
                               ):
    is_invalid_actual_tab = True if val_actual_tab is None else False
    match ctx.triggered_id:
        case 'btn_right':
            if not is_invalid_actual_tab:
                timeline.right_btn_triggered()
                timeline.set_actual_view(timeline.get_actual_tab())

        case 'btn_left':
            if not is_invalid_actual_tab:
                timeline.left_btn_triggered()
                timeline.set_actual_view(timeline.get_actual_tab())

        case 'btn_right_end':
            if not is_invalid_actual_tab:
                timeline.right_end_btn_triggered()
                timeline.set_actual_view(timeline.get_actual_tab())

        case 'btn_left_end':
            if not is_invalid_actual_tab:
                timeline.left_end_btn_triggered()
                timeline.set_actual_view(timeline.get_actual_tab())

        case 'btn_summary':
            min_fig: datetime = timeline.get_minimum_time()
            max_fig: datetime = timeline.get_maximum_time()
            return (timeline.get_figure().update_xaxes(range=[min_fig, max_fig]),
                    timeline.get_actual_tab(),
                    actual_tab_max,
                    f'/{timeline.get_tot_tabs()}',
                    set_step_graph_max_value_hint,
                    val_set_step_graph,
                    set_step_graph_max,
                    False,
                    None,
                    False,
                    None,
                    start_time_sim, finish_time_sim, total_time_sim,
                    output_stats_actions_started,
                    output_stats_actions_started_data_table,
                    output_stats_actions_started_figure,
                    output_stats_actions_finished,
                    output_stats_actions_finished_data_table,
                    output_stats_actions_finished_figure,
                    output_stats_actions_completed,
                    output_stats_actions_completed_data_table,
                    output_stats_actions_completed_figure)

        case 'actual_tab':
            if not is_invalid_actual_tab:
                timeline.set_actual_view(val_actual_tab)
            return (timeline.get_figure().update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
                    val_actual_tab,
                    actual_tab_max,
                    f'/{timeline.get_tot_tabs()}',
                    set_step_graph_max_value_hint,
                    val_set_step_graph,
                    set_step_graph_max,
                    False,
                    None,
                    False,
                    None,
                    start_time_sim, finish_time_sim, total_time_sim,
                    output_stats_actions_started,
                    output_stats_actions_started_data_table,
                    output_stats_actions_started_figure,
                    output_stats_actions_finished,
                    output_stats_actions_finished_data_table,
                    output_stats_actions_finished_figure,
                    output_stats_actions_completed,
                    output_stats_actions_completed_data_table,
                    output_stats_actions_completed_figure)

        case 'set_step_graph':
            if val_set_step_graph is not None:
                timeline.set_step(val_set_step_graph)
            return (timeline.get_figure().update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
                    timeline.get_actual_tab(),
                    actual_tab_max,
                    f'/{timeline.get_tot_tabs()}',
                    set_step_graph_max_value_hint,
                    val_set_step_graph,
                    set_step_graph_max,
                    False,
                    None,
                    False,
                    None,
                    start_time_sim, finish_time_sim, total_time_sim,
                    output_stats_actions_started,
                    output_stats_actions_started_data_table,
                    output_stats_actions_started_figure,
                    output_stats_actions_finished,
                    output_stats_actions_finished_data_table,
                    output_stats_actions_finished_figure,
                    output_stats_actions_completed,
                    output_stats_actions_completed_data_table,
                    output_stats_actions_completed_figure)

        case 'btn_new_simulation':
            # run new simulation if there are no probs
            if fields_new_simulation_are_valid(
                    FieldsNewSimulationArgs(
                        num_actions_sim, num_drawers_sim, num_materials_sim, checkbox_time_sim, time_sim
                    )
            ):
                # check if a checkbox (deposit/buffer drawer) has been triggered
                checklist_generators = {} if checklist_generators is None else checklist_generators
                if time_sim is not None:
                    time_converted = datetime.strptime(time_sim, '%H:%M:%S')
                    time_sim = time_converted.second + (time_converted.minute * 60) + ((time_converted.hour * 60) * 60)
                start_sim = datetime.now()
                warehouse.new_simulation(num_actions=num_actions_sim,
                                         num_gen_drawers=num_drawers_sim,
                                         num_gen_materials=num_materials_sim,
                                         gen_deposit=True if 'gen_deposit' in checklist_generators else False,
                                         gen_buffer=True if 'gen_buffer' in checklist_generators else False,
                                         time=time_sim)
                end_sim = datetime.now()
                history = warehouse.get_simulation().get_store_history().items
                if len(history) == 0:
                    return (timeline_old, timeline.get_actual_tab(), actual_tab_max, f'/{timeline.get_tot_tabs()}',
                            set_step_graph_max_value_hint, val_set_step_graph, set_step_graph_max, False, None, True,
                            "The time set is too low. Please try again by setting a higher value (or remove the time).",
                            start_time_sim, finish_time_sim, total_time_sim)
                timeline.__init__(history)
                # check the view range, because if you set 10 min (e.g.) and you run a new simulation,
                # the range is updated in this way
                if val_set_step_graph is not None:
                    timeline.set_step(
                        val_set_step_graph if val_set_step_graph <= timeline.get_tot_tabs() else timeline.get_tot_tabs())
                    timeline.get_figure().update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()])
                # statistics calculations
                warehouse_statistics.__init__(DataFrame(history))
                total_simulation_time = warehouse_statistics.total_simulation_time()
                # started
                type_of_action_selected_started: ActionEnum | None = ActionEnum.from_str(output_stats_actions_started.split(" ")[-1])
                actions_started_every_hour: DataFrame = (
                    warehouse_statistics.actions_started_every(TimeEnum.HOUR) if type_of_action_selected_started is None
                    else warehouse_statistics.action_started_every(type_of_action_selected_started, TimeEnum.HOUR)
                )
                # finished
                type_of_action_selected_finished: ActionEnum | None = ActionEnum.from_str(
                    output_stats_actions_finished.split(" ")[-1])
                actions_finished_every_hour: DataFrame = (
                    warehouse_statistics.actions_finished_every(TimeEnum.HOUR) if type_of_action_selected_finished is None
                    else warehouse_statistics.action_finished_every(type_of_action_selected_finished, TimeEnum.HOUR)
                )
                # completed
                type_of_action_selected_completed: ActionEnum | None = ActionEnum.from_str(
                    output_stats_actions_completed.split(" ")[-1])
                actions_completed_every_hour: DataFrame = (
                    warehouse_statistics.actions_completed_every(TimeEnum.HOUR) if type_of_action_selected_completed is None
                    else warehouse_statistics.action_completed_every(type_of_action_selected_completed, TimeEnum.HOUR)
                )

                return (timeline.get_figure(), 1, timeline.get_tot_tabs(), f'/{timeline.get_tot_tabs()}',
                        f'Max value: {timeline.get_tot_tabs() * timeline.get_step()} min.', timeline.get_step(),
                        timeline.get_tot_tabs() * timeline.get_step(),
                        True, f"Simulation completed in {end_sim - start_sim} (hh:mm:ss)", False, None,
                        warehouse_statistics.start_time_simulation().strftime('%a %d %b %Y, %H:%M:%S'),
                        warehouse_statistics.finish_time_simulation().strftime('%a %d %b %Y, %H:%M:%S'),
                        f"{total_simulation_time.days} days, "
                        f"{str(total_simulation_time.components.hours).zfill(2)}:"
                        f"{str(total_simulation_time.components.minutes).zfill(2)}:"
                        f"{str(total_simulation_time.components.seconds).zfill(2)}",
                        # stats:
                        # started
                        f"Show data of the action: {type_of_action_selected_started}",
                        dbc.Table.from_dataframe(actions_started_every_hour),
                        go.Figure(data=[go.Scatter(x=actions_started_every_hour['Start'],
                                                   y=actions_started_every_hour['Count'])]),
                        # finished
                        f"Show data of the action: {type_of_action_selected_finished}",
                        dbc.Table.from_dataframe(actions_finished_every_hour),
                        go.Figure(data=[go.Scatter(x=actions_finished_every_hour['Finish'],
                                                   y=actions_finished_every_hour['Count'])]),
                        # completed
                        f"Show data of the action: {type_of_action_selected_completed}",
                        dbc.Table.from_dataframe(actions_completed_every_hour),
                        go.Figure(data=[go.Scatter(y=[f"{actions_completed_every_hour['Start'][i]} - "
                                                      f"{actions_completed_every_hour['Finish'][i]}"
                                                      for i in range(actions_completed_every_hour['Count'].size)],
                                                   x=actions_completed_every_hour['Count'])])
                        )

            return (timeline_old, timeline.get_actual_tab(), actual_tab_max, f'/{timeline.get_tot_tabs()}',
                    set_step_graph_max_value_hint, val_set_step_graph, set_step_graph_max, False, None, False, None,
                    start_time_sim, finish_time_sim, total_time_sim,
                    output_stats_actions_started,
                    output_stats_actions_started_data_table,
                    output_stats_actions_started_figure,
                    output_stats_actions_finished,
                    output_stats_actions_finished_data_table,
                    output_stats_actions_finished_figure,
                    output_stats_actions_completed,
                    output_stats_actions_completed_data_table,
                    output_stats_actions_completed_figure)

    return (timeline.get_figure().update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
            timeline.get_actual_tab(),
            actual_tab_max,
            f'/{timeline.get_tot_tabs()}',
            set_step_graph_max_value_hint,
            val_set_step_graph,
            set_step_graph_max,
            False,
            None,
            False,
            None,
            start_time_sim, finish_time_sim, total_time_sim,
            output_stats_actions_started, output_stats_actions_started_data_table, output_stats_actions_started_figure,
            output_stats_actions_finished,
            output_stats_actions_finished_data_table,
            output_stats_actions_finished_figure,
            output_stats_actions_completed,
            output_stats_actions_completed_data_table,
            output_stats_actions_completed_figure
            )


@app.callback(
    Output('set_step_graph', 'invalid'),
    Input('set_step_graph', 'value'),
    prevent_initial_call=True
)
@cache.memoize()
def invalid_set_step_graph(set_step_graph_val):
    return True if set_step_graph_val is None else False


@app.callback(
    Output('actual_tab', 'invalid'),
    Input('actual_tab', 'value'),
    prevent_initial_call=True
)
@cache.memoize()
def invalid_actual_tab(actual_tab_val):
    return True if actual_tab_val is None else False


@app.callback(
    Output('num_actions_sim', 'invalid'),
    Input('num_actions_sim', 'value'),
    Input('btn_new_simulation', 'n_clicks'),
    prevent_initial_call=True
)
@cache.memoize()
def invalid_num_actions_sim(num_actions_sim_val, btn_new_simulation_val):
    return True if num_actions_sim_val is None else False


@app.callback(
    Output('num_drawers_sim', 'invalid'),
    Input('num_drawers_sim', 'value'),
    Input('btn_new_simulation', 'n_clicks'),
    prevent_initial_call=True
)
@cache.memoize()
def invalid_num_drawers_sim(num_drawers_sim_val, btn_new_simulation_val):
    return True if num_drawers_sim_val is None else False


@app.callback(
    Output('num_materials_sim', 'invalid'),
    Input('num_materials_sim', 'value'),
    Input('btn_new_simulation', 'n_clicks'),
    prevent_initial_call=True
)
@cache.memoize()
def invalid_num_materials_sim(num_materials_sim_val, btn_new_simulation_val):
    return True if num_materials_sim_val is None else False


@app.callback(
    Output('time_sim', 'readonly'),
    Output('time_sim', 'value'),
    Input('checkbox_time_sim', 'value'),
    prevent_initial_call=True
)
@cache.memoize()
def readonly_input_checkbox_time_sim(checkbox_time_sim_val):
    return not checkbox_time_sim_val, None


@app.callback(
    Output('time_sim', 'invalid'),
    Input('time_sim', 'value'),
    State('time_sim', 'readonly'),
    prevent_initial_call=True
)
@cache.memoize()
def invalid_time_sim(time_sim_val, time_sim_readonly):
    if not time_sim_readonly:
        return True if (time_sim_val is None or time_sim_val == "00:00:00") else False

@app.callback(
    Output("config-show_col", "children"),
    Input("config-choose_col", "value"),
    prevent_initial_call=True
)
def config_show_cols(col):
    return create_columns_layout(num_col=int(col.removeprefix('Column '))-1)


@app.callback(
    Output("num_action_sim_stats", "children"),
    Output("drawers_to_gen_sim_stats", "children"),
    Output("materials_to_gen_sim_stats", "children"),
    Output("gen_deposit_sim_stats", "children"),
    Output("gen_buffer_sim_stats", "children"),
    Output("total_time_sim_stats", "children"),

    Input("btn_new_simulation", "n_clicks"),
    State('num_actions_sim', 'value'),
    State('num_drawers_sim', 'value'),
    State('num_materials_sim', 'value'),
    State('checkbox_time_sim', 'value'),
    State('time_sim', 'value'),
    State('checklist_generators', 'value'),
    prevent_initial_call=True
)
@cache.memoize()
def stats_number_of_simulated_actions_requested(
        btn_new_simulation,
        num_actions_sim,
        num_drawers_sim,
        num_materials_sim,
        checkbox_time_sim,
        time_sim,
        checklist_generators
):
    if fields_new_simulation_are_valid(
            FieldsNewSimulationArgs(num_actions_sim, num_drawers_sim, num_materials_sim, checkbox_time_sim, time_sim)
    ):
        return (num_actions_sim, num_drawers_sim, num_materials_sim,
                'True' if 'gen_deposit' in
                          (checklist_generators := {} if checklist_generators is None else checklist_generators)
                else 'False',
                'True' if 'gen_buffer' in checklist_generators else 'False',
                time_sim if time_sim is not None else 'Not specified')

    raise PreventUpdate


@app.callback(
    Output("output_stats-actions_started", "label", allow_duplicate=True),
    Output("output_stats-actions_started-data_table", "children", allow_duplicate=True),
    Output("output_stats-actions_started-figure", "figure", allow_duplicate=True),
    Input("output_stats-actions_started-none", "n_clicks"),
    Input("output_stats-actions_started-ExtractDrawer", "n_clicks"),
    Input("output_stats-actions_started-SendBackDrawer", "n_clicks"),
    Input("output_stats-actions_started-InsertRandomMaterial", "n_clicks"),
    Input("output_stats-actions_started-RemoveRandomMaterial", "n_clicks"),
    prevent_initial_call=True
)
def output_stats_actions_started_menu_triggered(none,
                                                extract_drawer,
                                                send_back_drawer,
                                                insert_random_material,
                                                remove_random_material
                                                ):
    type_of_action: ActionEnum | None = ActionEnum.from_str(ctx.triggered_id.split("-")[-1])
    data: DataFrame = (
        warehouse_statistics.actions_started_every(TimeEnum.HOUR) if type_of_action is None
        else warehouse_statistics.action_started_every(type_of_action, TimeEnum.HOUR)
    )
    return (f"Show data of the action: {type_of_action}",
            dbc.Table.from_dataframe(data),
            go.Figure(data=[go.Scatter(x=data['Start'],
                                       y=data['Count'])])
            )


@app.callback(
    Output("output_stats-actions_finished", "label", allow_duplicate=True),
    Output("output_stats-actions_finished-data_table", "children", allow_duplicate=True),
    Output("output_stats-actions_finished-figure", "figure", allow_duplicate=True),
    Input("output_stats-actions_finished-none", "n_clicks"),
    Input("output_stats-actions_finished-ExtractDrawer", "n_clicks"),
    Input("output_stats-actions_finished-SendBackDrawer", "n_clicks"),
    Input("output_stats-actions_finished-InsertRandomMaterial", "n_clicks"),
    Input("output_stats-actions_finished-RemoveRandomMaterial", "n_clicks"),
    prevent_initial_call=True
)
def output_stats_actions_finished_menu_triggered(none,
                                                 extract_drawer,
                                                 send_back_drawer,
                                                 insert_random_material,
                                                 remove_random_material
                                                 ):
    type_of_action: ActionEnum | None = ActionEnum.from_str(ctx.triggered_id.split("-")[-1])
    data: DataFrame = (
        warehouse_statistics.actions_finished_every(TimeEnum.HOUR) if type_of_action is None
        else warehouse_statistics.action_finished_every(type_of_action, TimeEnum.HOUR)
    )
    return (f"Show data of the action: {type_of_action}",
            dbc.Table.from_dataframe(data),
            go.Figure(data=[go.Scatter(x=data['Finish'],
                                       y=data['Count'])])
            )


@app.callback(
    Output("output_stats-actions_completed", "label", allow_duplicate=True),
    Output("output_stats-actions_completed-data_table", "children", allow_duplicate=True),
    Output("output_stats-actions_completed-figure", "figure", allow_duplicate=True),
    Input("output_stats-actions_completed-none", "n_clicks"),
    Input("output_stats-actions_completed-ExtractDrawer", "n_clicks"),
    Input("output_stats-actions_completed-SendBackDrawer", "n_clicks"),
    Input("output_stats-actions_completed-InsertRandomMaterial", "n_clicks"),
    Input("output_stats-actions_completed-RemoveRandomMaterial", "n_clicks"),
    prevent_initial_call=True
)
def output_stats_actions_completed_menu_triggered(none,
                                                 extract_drawer,
                                                 send_back_drawer,
                                                 insert_random_material,
                                                 remove_random_material
                                                 ):
    type_of_action: ActionEnum | None = ActionEnum.from_str(ctx.triggered_id.split("-")[-1])
    data: DataFrame = (
        warehouse_statistics.actions_completed_every(TimeEnum.HOUR) if type_of_action is None
        else warehouse_statistics.action_completed_every(type_of_action, TimeEnum.HOUR)
    )
    return (f"Show data of the action: {type_of_action}",
            dbc.Table.from_dataframe(data),
            go.Figure(
                data=[go.Scatter(
                    y=[f"{data['Start'][i]} - "
                       f"{data['Finish'][i]}"
                       for i in range(data['Count'].size)],
                    x=data['Count']
                )])
            )


@app.callback(
    Output("download-stats", "data"),
    Input("download_data-xlsx-output_stats-actions_started", "n_clicks"),
    Input("download_data-csv-output_stats-actions_started", "n_clicks"),
    Input("download_scatter-svg-output_stats-actions_started", "n_clicks"),
    Input("download_scatter-pdf-output_stats-actions_started", "n_clicks"),
    State("output_stats-actions_started", "label"),
    prevent_initial_call=True
)
def download_output_stats_actions_started(b_data_xlsx, b_data_csv, b_scatter_svg, b_scatter_pdf, action_selected):
    action: ActionEnum | None = ActionEnum.from_str(action_selected.split(" ")[-1])
    file_path = f"./images/graph_stats-actions_started" if action is None else f"./images/graph_stats-action_{action}_started"
    extension = ''
    data: DataFrame = (warehouse_statistics.actions_started_every(TimeEnum.HOUR) if action is None
            else warehouse_statistics.action_started_every(action, TimeEnum.HOUR))
    # which button is triggered?
    match ctx.triggered_id:
        case "download_data-xlsx-output_stats-actions_started":
            data.to_excel(f"{file_path}.xlsx")
            return dcc.send_file(f"{file_path}.xlsx")
        case "download_data-csv-output_stats-actions_started":
            data.to_csv(f"{file_path}.csv")
            return dcc.send_file(f"{file_path}.csv")
        case "download_scatter-svg-output_stats-actions_started":
            extension = 'svg'
        case "download_scatter-pdf-output_stats-actions_started":
            extension = 'pdf'
        case _:
            raise PreventUpdate
    # create the file
    with open(f"{file_path}.{extension}", "w"):
        pass
    # take graph to download
    go.Figure(
        data=[go.Scatter(x=data['Start'],
                         y=data['Count'])]).write_image(
        f"{file_path}.{extension}", engine='kaleido', width=1920, height=1080
    )
    return dcc.send_file(
        f"{file_path}.{extension}"
    )


@app.callback(
    Output("download-stats", "data", allow_duplicate=True),
    Input("download_data-xlsx-output_stats-actions_finished", "n_clicks"),
    Input("download_data-csv-output_stats-actions_finished", "n_clicks"),
    Input("download_scatter-svg-output_stats-actions_finished", "n_clicks"),
    Input("download_scatter-pdf-output_stats-actions_finished", "n_clicks"),
    State("output_stats-actions_finished", "label"),
    prevent_initial_call=True
)
def download_output_stats_actions_started(b_data_xlsx, b_data_csv, b_scatter_svg, b_scatter_pdf, action_selected):
    action: ActionEnum | None = ActionEnum.from_str(action_selected.split(" ")[-1])
    file_path = f"./images/graph_stats-actions_finished" if action is None else f"./images/graph_stats-action_{action}_finished"
    extension = ''
    data: DataFrame = (warehouse_statistics.actions_finished_every(TimeEnum.HOUR) if action is None
            else warehouse_statistics.action_finished_every(action, TimeEnum.HOUR))
    # which button is triggered?
    match ctx.triggered_id:
        case "download_data-xlsx-output_stats-actions_finished":
            data.to_excel(f"{file_path}.xlsx")
            return dcc.send_file(f"{file_path}.xlsx")
        case "download_data-csv-output_stats-actions_finished":
            data.to_csv(f"{file_path}.csv")
            return dcc.send_file(f"{file_path}.csv")
        case "download_scatter-svg-output_stats-actions_finished":
            extension = 'svg'
        case "download_scatter-pdf-output_stats-actions_finished":
            extension = 'pdf'
        case _:
            raise PreventUpdate
    # create the file
    with open(f"{file_path}.{extension}", "w"):
        pass
    # take graph to download
    go.Figure(
        data=[go.Scatter(x=data['Finish'],
                         y=data['Count'])]).write_image(
        f"{file_path}.{extension}", engine='kaleido', width=1920, height=1080
    )
    return dcc.send_file(
        f"{file_path}.{extension}"
    )


@app.callback(
    Output("download-stats", "data", allow_duplicate=True),
    Input("download_data-xlsx-output_stats-actions_completed", "n_clicks"),
    Input("download_data-csv-output_stats-actions_completed", "n_clicks"),
    Input("download_scatter-svg-output_stats-actions_completed", "n_clicks"),
    Input("download_scatter-pdf-output_stats-actions_completed", "n_clicks"),
    State("output_stats-actions_completed", "label"),
    prevent_initial_call=True
)
def download_output_stats_actions_started(b_data_xlsx, b_data_csv, b_scatter_svg, b_scatter_pdf, action_selected):
    action: ActionEnum | None = ActionEnum.from_str(action_selected.split(" ")[-1])
    file_path = f"./images/graph_stats-actions_completed" if action is None else f"./images/graph_stats-action_{action}_completed"
    extension = ''
    data: DataFrame = (warehouse_statistics.actions_completed_every(TimeEnum.HOUR) if action is None
            else warehouse_statistics.action_completed_every(action, TimeEnum.HOUR))
    # which button is triggered?
    match ctx.triggered_id:
        case "download_data-xlsx-output_stats-actions_completed":
            data.to_excel(f"{file_path}.xlsx")
            return dcc.send_file(f"{file_path}.xlsx")
        case "download_data-csv-output_stats-actions_completed":
            data.to_csv(f"{file_path}.csv")
            return dcc.send_file(f"{file_path}.csv")
        case "download_scatter-svg-output_stats-actions_completed":
            extension = 'svg'
        case "download_scatter-pdf-output_stats-actions_completed":
            extension = 'pdf'
        case _:
            raise PreventUpdate
    # create the file
    with open(f"{file_path}.{extension}", "w"):
        pass
    # take graph to download
    go.Figure(
        data=[go.Scatter(y=[f"{data['Start'][i]} - {data['Finish'][i]}" for i in range(data['Count'].size)],
                         x=data['Count'])]).write_image(
        f"{file_path}.{extension}", engine='kaleido', width=1920, height=1080
    )
    return dcc.send_file(
        f"{file_path}.{extension}"
    )


def _signal_handler(frame, sig):
    print("Removing cache folder")
    try:
        shutil.rmtree("cache/")
    except FileNotFoundError:
        print("Cache folder doesn't exist")
    sys.exit(0)


if __name__ == '__main__':
    signal(SIGINT, _signal_handler)
    signal(SIGTERM, _signal_handler)
    app.run(host=HOST, port=PORT, proxy=PROXY, debug=False)
