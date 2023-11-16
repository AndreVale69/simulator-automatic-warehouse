# Run this app with `python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# from dash_bootstrap_templates import ThemeSwitchAIO, load_figure_template
# from datetime import datetime, timedelta, date
# import dash_daq as daq
# from dash_bootstrap_templates import load_figure_template

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

from dash import Dash, dcc, html, Input, Output, ctx, State
from simpy import Store
from pandas import Timestamp
from datetime import datetime

from src.sim.warehouse import Warehouse
from collections import Counter
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
# Import bootstrap components
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
app = Dash(external_stylesheets=[BS, dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           # this ensures that mobile devices don't rescale your content on small screens
           # and lets you build mobile optimised layouts
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])


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
                children='Warehouse simulator',
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
                                dbc.Input(id='num_actions_sim', type='number', min=1, step=1, placeholder='# Actions', required=True) # TODO: add '?' and write in what does it means. You can use also 'info' icon (boostrap)
                            ]),
                            dbc.ListGroupItem([
                                dbc.Label('Total number of drawers:'),
                                dbc.Input(id='num_drawers_sim', type='number', min=1, step=1, placeholder='# Drawers')
                            ]),
                            dbc.ListGroupItem([
                                dbc.Label('Total number of materials:'),
                                dbc.Input(id='num_materials_sim', type='number', min=1, step=1, placeholder='# Materials')
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
                                    dbc.Input(id='time_sim', type='number', min=1, step=1, placeholder='Seconds', readonly=True)
                                ]),
                            ])
                        ])
                    ]),

                    dbc.CardFooter([
                        dbc.Col([
                            dbc.Button(children='Run new simulation!', id='btn_new_simulation', n_clicks=0)
                        ], width={'offset': 2})
                    ]),
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
                            dbc.Row([
                                dcc.Graph(
                                    id='graph-actions',
                                    figure=timeline.get_figure()
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
        dcc.Download(id="download-graph")
    ])

app.layout = serve_layout

""" 
    ##########################
    * Application's callback * 
    ##########################
"""
@app.callback(
    Output("download-graph", "data"),
    [Input("dropdown-btn_svg", "n_clicks"),
    Input("dropdown-btn_pdf", "n_clicks")],
    prevent_initial_call=True
)
def download_graph(b_svg, b_pdf):
    extension = ''
    # which button is triggered?
    if "dropdown-btn_svg" == ctx.triggered_id:
        extension = 'svg'
    elif "dropdown-btn_pdf" == ctx.triggered_id:
        extension = 'pdf'
    # take graph to download
    timeline.get_figure().write_image(f"./images/graph_actions.{extension}", engine='kaleido', width=1920, height=1080)
    return dcc.send_file(
        f"./images/graph_actions.{extension}"
    )


@app.callback(
    Output('graph-actions', 'figure'),
    Output('actual_tab', 'value'),
    Output('num_tabs_graph', 'children'),

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
    prevent_initial_call=True
)
def update_timeline_components(val_btn_right, val_btn_left, val_btn_right_end, val_btn_left_end, val_btn_summary,
                               val_actual_tab, val_set_step_graph,
                               # trigger new simulation button
                               clicks_btn,
                               num_actions_sim, num_drawers_sim, num_materials_sim,
                               checklist_generators, checkbox_time_sim,
                               time_sim,
                               timeline_old
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
                    f'/{timeline.get_tot_tabs()}')

        case 'actual_tab':
            if not is_invalid_actual_tab:
                timeline.set_actual_view(val_actual_tab)
            return (timeline.get_figure().update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
                    val_actual_tab,
                    f'/{timeline.get_tot_tabs()}')

        case 'set_step_graph':
            if val_set_step_graph is not None:
                timeline.set_step(val_set_step_graph)
            return (timeline.get_figure().update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
                    timeline.get_actual_tab(),
                    f'/{timeline.get_tot_tabs()}')

        case 'btn_new_simulation':
            return exec_new_simulation(clicks_btn,
                        num_actions_sim, num_drawers_sim, num_materials_sim,
                        checklist_generators, checkbox_time_sim,
                        time_sim,
                        timeline_old), timeline.get_actual_tab(), f'/{timeline.get_tot_tabs()}'

    return (timeline.get_figure().update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
            timeline.get_actual_tab(),
            f'/{timeline.get_tot_tabs()}')


@app.callback(
    Output('set_step_graph', 'invalid'),
    Input('set_step_graph', 'value'),
    prevent_initial_call=True
)
def invalid_set_step_graph(set_step_graph_val):
    return True if set_step_graph_val is None else False


@app.callback(
    Output('actual_tab', 'invalid'),
    Input('actual_tab', 'value'),
    prevent_initial_call=True
)
def invalid_actual_tab(actual_tab_val):
    return True if actual_tab_val is None else False


@app.callback(
    Output('num_actions_sim', 'invalid'),
    Input('num_actions_sim', 'value'),
    Input('btn_new_simulation', 'n_clicks'),
    prevent_initial_call=True
)
def invalid_num_actions_sim(num_actions_sim_val, btn_new_simulation_val):
    return True if num_actions_sim_val is None else False


@app.callback(
    Output('num_drawers_sim', 'invalid'),
    Input('num_drawers_sim', 'value'),
    Input('btn_new_simulation', 'n_clicks'),
    prevent_initial_call=True
)
def invalid_num_drawers_sim(num_drawers_sim_val, btn_new_simulation_val):
    return True if num_drawers_sim_val is None else False


@app.callback(
    Output('num_materials_sim', 'invalid'),
    Input('num_materials_sim', 'value'),
    Input('btn_new_simulation', 'n_clicks'),
    prevent_initial_call=True
)
def invalid_num_materials_sim(num_materials_sim_val, btn_new_simulation_val):
    return True if num_materials_sim_val is None else False


@app.callback(
    Output('time_sim', 'readonly'),
    Output('time_sim', 'value'),
    Input('checkbox_time_sim', 'value'),
    prevent_initial_call=True
)
def readonly_input_checkbox_time_sim(checkbox_time_sim_val):
    return not checkbox_time_sim_val, None


@app.callback(
    Output('time_sim', 'invalid'),
    Input('time_sim', 'value'),
    State('time_sim', 'readonly'),
    prevent_initial_call=True
)
def invalid_time_sim(time_sim_val, time_sim_readonly):
    if not time_sim_readonly:
        return True if time_sim_val is None else False


# TODO: Found bug! If you put 'graph-actions' id inside the Output, it will be a conflict!
#       The callback connected to 'update_timeline_components' function has 'graph-actions' as Output id.
#       So you must merge these two functions (update_timeline_components and exec_new_simulation).
#       In this beta, you can see the new timeline (at the end of the page)
def exec_new_simulation(clicks_btn,
                        num_actions_sim, num_drawers_sim, num_materials_sim,
                        checklist_generators, checkbox_time_sim,
                        time_sim,
                        timeline_old) -> go.Figure:
    # check if actions number is invalid
    actions_invalid = True if num_actions_sim is None else False
    # check if drawers number is invalid
    drawers_invalid = True if num_drawers_sim is None else False
    # check if materials number is invalid
    materials_invalid = True if num_materials_sim is None else False
    # check if a checkbox (deposit/buffer drawer) has been triggered
    checklist_generators = {} if checklist_generators is None else checklist_generators
    # check if a time of the simulation has been triggered and if the time value is not None
    time_sim_invalid = True if (checkbox_time_sim and time_sim is None) else False

    # run new simulation if there are no probs
    if not actions_invalid and not drawers_invalid and not materials_invalid and not time_sim_invalid:
        warehouse.new_simulation(num_actions=num_actions_sim,
                                 num_gen_drawers=num_drawers_sim,
                                 num_gen_materials=num_materials_sim,
                                 gen_deposit=True if 'gen_deposit' in checklist_generators else False,
                                 gen_buffer=True if 'gen_buffer' in checklist_generators else False,
                                 time=time_sim if time_sim != False else None)
        timeline = Timeline(warehouse.get_simulation().get_store_history().items)
        return timeline.get_figure()

    return timeline_old


if __name__ == '__main__':
    app.run_server(debug=False)
