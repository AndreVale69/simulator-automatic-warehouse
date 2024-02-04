# Run this app with `python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
import diskcache

from dash import Dash, dcc, html, Input, Output, ctx, State, DiskcacheManager
from datetime import datetime
from dash.exceptions import PreventUpdate
from collections import Counter

from src.sim.warehouse import Warehouse
from web_app.components.timeline import Timeline

"""
    #####################
    * Set-up simulation *
    #####################
"""

# Initialize the Warehouse for simulation
warehouse = Warehouse()
warehouse.run_simulation()
cn = Counter(warehouse.get_events_to_simulate())

"""
    #########################
    * Set-up all components *
    #########################
"""
# documentation: https://dash.plotly.com/background-callbacks
# from dash import CeleryManager
# if 'REDIS_URL' in os.environ:
#     # Use Redis & Celery if REDIS_URL set as an env variable
#     from celery import Celery
#
#     celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
#     background_callback_manager = CeleryManager(celery_app)
# else:
#     # Diskcache for non-production apps when developing locally
#     import diskcache
#
#     cache = diskcache.Cache("./cache")
#     background_callback_manager = DiskcacheManager(cache)
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

# Import bootstrap components
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
app = Dash(external_stylesheets=[BS, dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           # this ensures that mobile devices don't rescale your content on small screens
           # and lets you build mobile optimised layouts
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
           background_callback_manager=background_callback_manager)

# timeline manager
timeline = Timeline(warehouse.get_simulation().get_store_history().items)

""" 
    ########################
    * Application's layout * 
    ########################
"""


def serve_layout():
    # see live updates on: https://dash.plotly.com/live-updates
    return html.Div(children=[
        dbc.Row([
            html.H1(
                children='Automatic Warehouse Simulator',
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
        dcc.Download(id="download-graph"),
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
        )
    ])


app.layout = serve_layout

""" 
    ##########################
    * Application's callback * 
    ##########################
"""


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
    # check if actions number is invalid
    actions_invalid = True if num_actions_sim is None else False
    # check if drawers number is invalid
    drawers_invalid = True if num_drawers_sim is None else False
    # check if materials number is invalid
    materials_invalid = True if num_materials_sim is None else False
    # check if a time of the simulation has been triggered and if the time value is not None
    time_sim_invalid = True if (checkbox_time_sim and time_sim is None) else False

    if not actions_invalid and not drawers_invalid and not materials_invalid and not time_sim_invalid:
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
    [Input("dropdown-btn_svg", "n_clicks"),
     Input("dropdown-btn_pdf", "n_clicks")],
    prevent_initial_call=True
)
def download_graph(b_svg, b_pdf):
    extension = ''
    # which button is triggered?
    match ctx.triggered_id:
        case "dropdown-btn_svg":
            extension = 'svg'
        case "dropdown-btn_pdf":
            extension = 'pdf'
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
                               actual_tab_max
                               ):
    # Use switch case because is more efficiently than if-else
    # Source: https://www.geeksforgeeks.org/switch-vs-else/
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
                    None)

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
                    None)

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
                    None)

        case 'btn_new_simulation':
            # check if actions number is invalid
            actions_invalid = True if num_actions_sim is None else False
            # check if drawers number is invalid
            drawers_invalid = True if num_drawers_sim is None else False
            # check if materials number is invalid
            materials_invalid = True if num_materials_sim is None else False
            # check if a checkbox (deposit/buffer drawer) has been triggered
            checklist_generators = {} if checklist_generators is None else checklist_generators
            # check if a time of the simulation has been triggered and if the time value is not None
            time_sim_invalid = True if (checkbox_time_sim and (time_sim is None or time_sim == "00:00:00")) else False

            # run new simulation if there are no probs
            if not actions_invalid and not drawers_invalid and not materials_invalid and not time_sim_invalid:
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
                            "The time set is too low. Please try again by setting a higher value (or remove the time).")
                timeline.__init__(history)
                # check the view range, because if you set 10 min (e.g.) and you run a new simulation,
                # the range is updated in this way
                if val_set_step_graph is not None:
                    timeline.set_step(
                        val_set_step_graph if val_set_step_graph <= timeline.get_tot_tabs() else timeline.get_tot_tabs())
                    timeline.get_figure().update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()])
                return (timeline.get_figure(), 1, timeline.get_tot_tabs(), f'/{timeline.get_tot_tabs()}',
                        f'Max value: {timeline.get_tot_tabs() * timeline.get_step()} min.', timeline.get_step(),
                        timeline.get_tot_tabs() * timeline.get_step(),
                        True, f"Simulation completed in {end_sim - start_sim} (hh:mm:ss)", False, None)

            return (timeline_old, timeline.get_actual_tab(), actual_tab_max, f'/{timeline.get_tot_tabs()}',
                    set_step_graph_max_value_hint, val_set_step_graph, set_step_graph_max, False, None, False, None)

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
            None)


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


if __name__ == '__main__':
    app.run_server(debug=True)
