# Run this app with `python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# from dash_bootstrap_templates import ThemeSwitchAIO, load_figure_template
# from datetime import datetime, timedelta, date
# import dash_daq as daq
# from dash_bootstrap_templates import load_figure_template

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

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

# See https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Actions": ["Send back a drawer", "Extract a drawer", "Insert material", "Remove material"],
#     "Nums Executions": [cn.get("send_back"), cn.get("extract_drawer"), cn.get("ins_mat"), cn.get("rmv_mat")]
# })

# fig = px.bar(df, x="Actions", y="Nums Executions", barmode="stack",
#              title='Number of actions performed', color='Actions')

#prova = [
#    dict(Action="Job A", Start='2009-01-01', Finish='2009-02-28'),
#    dict(Action="Job B", Start='2009-03-05', Finish='2009-04-15'),
#    dict(Action="Job C", Start='2009-02-20', Finish='2009-05-30')
#]
#prova.append(dict(Action="Job D", Start='2009-02-20', Finish='2009-05-30'))

# Get the simulation history
store_obj: Store = warehouse.get_simulation().get_store_history()
history = list()
# Create a list of labels, so take only the Action name from the object "store_obj"
for index in range(store_obj.capacity):
    history.append(store_obj.get().value)


df = pd.DataFrame(history)

# Take the minimum and maximum time of the simulation
min_time_sim: Timestamp = df.min().get('Start')
max_time_sim: Timestamp = df.max().get('Finish')
timeline = Timeline(min_time_sim, max_time_sim)
# prova1 = min_time_sim.time()
# prova2 = max_time_sim.time()
# prova3 = min_time_sim.date()
# prova4 = max_time_sim.date()
# prova1_delta: timedelta = timedelta(hours=prova1.hour, minutes=prova1.minute, seconds=prova1.second, microseconds=prova1.microsecond)
# prova2_delta: timedelta = timedelta(hours=prova2.hour, minutes=prova2.minute, seconds=prova2.second, microseconds=prova2.microsecond)
# diff_days: timedelta = prova4 - prova3
# diff_hours: timedelta = prova2_delta - prova1_delta


# Create the timeline
fig = px.timeline(df,
                  x_start="Start", x_end="Finish", y="Action",
                  range_x=[timeline.get_actual_left(), timeline.get_actual_right()],
                  color="Action")
fig.update_yaxes(autorange="reversed") # otherwise, tasks are listed from the bottom up
# If you want a linear timeline:
# fig.layout.xaxis.type = 'linear'
fig.layout.xaxis.type = 'date'
# create slider
fig.update_xaxes(rangeslider = dict(visible=True, range=[min_time_sim,max_time_sim]))
# If you want a rangeselector to zoom on each section
# See more: https://plotly.com/python/range-slider/
# fig.update_xaxes(
#     rangeslider = dict(visible=True, range=[min_time_sim,max_time_sim]),
#     rangeselector = dict(
#         buttons = list([
#             dict(count = 1, label = "1m", step = "minute", stepmode = "backward"),
#             dict(count = 5, label = "5m", step = "minute", stepmode = "backward"),
#             dict(count = 10, label = "10m", step = "minute", stepmode = "todate"),
#             dict(step = "all")
#         ])
#     )
# )

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
                                            dbc.InputGroupText(id='num_tabs_graph', children=f'/{timeline.get_tot_tabs()}'), # TODO: fix its value when goes to the limit
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
                                    figure=fig
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
        dcc.Graph(id='prova', figure=fig)
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
    fig.write_image(f"./images/graph_actions.{extension}", engine='kaleido', width=1920, height=1080)
    return dcc.send_file(
        f"./images/graph_actions.{extension}"
    )


@app.callback(
    Output('graph-actions', 'figure'),
    Output('actual_tab', 'value'),
    Output('actual_tab', 'invalid'),
    Output('num_tabs_graph', 'children'),
    Output('set_step_graph', 'invalid'),

    Input('btn_right', 'n_clicks'),
    Input('btn_left', 'n_clicks'),
    Input('btn_right_end', 'n_clicks'),
    Input('btn_left_end', 'n_clicks'),
    Input('btn_summary', 'n_clicks'),

    Input('actual_tab', 'value'),
    Input('set_step_graph', 'value'),

    State('set_step_graph', 'invalid'),
    prevent_initial_call=True
)
def update_timeline_components(val_btn_right, val_btn_left, val_btn_right_end, val_btn_left_end, val_btn_summary,
                               val_actual_tab, val_set_step_graph, state_set_step_graph):
    # Use switch case because is more efficiently than if-else
    # Source: https://www.geeksforgeeks.org/switch-vs-else/
    invalid_actual_tab: bool = True if val_actual_tab is None else False
    match ctx.triggered_id:
        case 'btn_right':
            timeline.right_btn_triggered()
            if not invalid_actual_tab:
                timeline.set_actual_view(timeline.get_actual_tab())

        case 'btn_left':
            timeline.left_btn_triggered()
            if not invalid_actual_tab:
                timeline.set_actual_view(timeline.get_actual_tab())

        case 'btn_right_end':
            timeline.right_end_btn_triggered()
            if not invalid_actual_tab:
                timeline.set_actual_view(timeline.get_actual_tab())

        case 'btn_left_end':
            timeline.left_end_btn_triggered()
            if not invalid_actual_tab:
                timeline.set_actual_view(timeline.get_actual_tab())

        case 'btn_summary':
            min_fig: datetime = timeline.get_minimum_time()
            max_fig: datetime = timeline.get_maximum_time()
            return (fig.update_xaxes(range=[min_fig, max_fig]),
                    timeline.get_actual_tab(),
                    invalid_actual_tab,
                    f'/{timeline.get_tot_tabs()}',
                    state_set_step_graph)

        case 'actual_tab':
            if not invalid_actual_tab:
                timeline.set_actual_view(val_actual_tab)
            return (fig.update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
                    val_actual_tab,
                    invalid_actual_tab,
                    f'/{timeline.get_tot_tabs()}',
                    state_set_step_graph)

        case 'set_step_graph':
            invalid_val_set_step_graph = True if val_set_step_graph is None else False
            if not invalid_val_set_step_graph:
                timeline.set_step(val_set_step_graph)
            return (fig.update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
                    timeline.get_actual_tab(),
                    invalid_actual_tab,
                    f'/{timeline.get_tot_tabs()}',
                    invalid_val_set_step_graph)

    return (fig.update_xaxes(range=[timeline.get_actual_left(), timeline.get_actual_right()]),
            timeline.get_actual_tab(),
            invalid_actual_tab,
            f'/{timeline.get_tot_tabs()}',
            state_set_step_graph)


@app.callback(
    Output('num_actions_sim', 'value'),
    Output('num_drawers_sim', 'value'),
    Output('num_materials_sim', 'value'),
    Output('num_actions_sim', 'invalid'),
    Output('num_drawers_sim', 'invalid'),
    Output('num_materials_sim', 'invalid'),
    Output('time_sim', 'readonly'),
    Output('time_sim', 'value'),


    Input('num_actions_sim', 'value'),
    Input('num_drawers_sim', 'value'),
    Input('num_materials_sim', 'value'),
    Input('checklist_generators', 'value'),
    Input('checkbox_time_sim', 'value'),


    State('num_actions_sim', 'value'),
    State('num_drawers_sim', 'value'),
    State('num_materials_sim', 'value'),
    State('num_actions_sim', 'invalid'),
    State('num_drawers_sim', 'invalid'),
    State('num_materials_sim', 'invalid'),
    State('time_sim', 'readonly'),
    State('checkbox_time_sim', 'value'),
    State('checklist_generators', 'options'),
)
def update_new_sim_components(
        # Inputs:
        actions_val, drawers_val, materials_val, checklist_generators_val, checkbox_time_val,
        # States:
        actions_val_state, drawers_val_state, materials_val_state, actions_invalid_state, drawers_invalid_state,
        materials_invalid_state, checkbox_time_readonly, checkbox_time_value, checklist_generators_options):
    match ctx.triggered_id:
        case 'num_actions_sim':
            actions_invalid_state = True if actions_val is None else False

        case 'num_drawers_sim':
            drawers_invalid_state = True if drawers_val is None else False

        case 'num_materials_sim':
            materials_invalid_state = True if materials_val is None else False

        case 'checkbox_time_sim':
            checkbox_time_readonly = not checkbox_time_val
            checkbox_time_val = None

        # TODO: to rmv
        case 'checklist_generators':
            return (actions_val_state,
                    drawers_val_state,
                    materials_val_state,
                    actions_invalid_state,
                    drawers_invalid_state,
                    materials_invalid_state,
                    checkbox_time_readonly,
                    checkbox_time_val)

    return (actions_val_state,
            drawers_val_state,
            materials_val_state,
            actions_invalid_state,
            drawers_invalid_state,
            materials_invalid_state,
            checkbox_time_readonly,
            checkbox_time_val)


@app.callback(
    Output('time_sim', 'invalid'),
    Input('time_sim', 'value'),
    State('time_sim', 'readonly')
)
def update_time_sim_input(time_sim_val, time_sim_readonly):
    if not time_sim_readonly:
        return True if time_sim_val is None else False


# TODO: Found bug! If you put 'graph-actions' id inside the Output, it will be a conflict!
#       The callback connected to 'update_timeline_components' function has 'graph-actions' as Output id.
#       So you must merge these two functions (update_timeline_components and exec_new_simulation).
#       In this beta, you can see the new timeline (at the end of the page)
@app.callback(
    Output('prova', 'figure'),

    Input('btn_new_simulation', 'n_clicks'),

    State('num_actions_sim', 'value'), # TODO: to check
    State('num_drawers_sim', 'value'), # TODO: to check
    State('num_materials_sim', 'value'), # TODO: to check
    State('checklist_generators', 'value'), # TODO: opt
    State('checkbox_time_sim', 'value'), # TODO: opt
    State('time_sim', 'value'), # TODO: it depends from checkbox_time_sim
    State('graph-actions', 'figure')
)
def exec_new_simulation(clicks_btn, num_actions_sim, num_drawers_sim, num_materials_sim, checklist_generators, checkbox_time_sim, time_sim, timeline):
    actions_invalid = True if num_actions_sim is None else False
    drawers_invalid = True if num_drawers_sim is None else False
    materials_invalid = True if num_materials_sim is None else False
    checklist_generators = dict() if checklist_generators is None else checklist_generators
    time_sim_invalid = False
    if checkbox_time_sim:
        time_sim_invalid = True if time_sim is None else False

    # run new simulation if there are no probs
    if not actions_invalid and not drawers_invalid and not materials_invalid and not time_sim_invalid:
        warehouse.new_simulation(num_actions=num_actions_sim,
                                 num_gen_drawers=num_drawers_sim,
                                 num_gen_materials=num_materials_sim,
                                 gen_deposit=True if 'gen_deposit' in checklist_generators else False,
                                 gen_buffer=True if 'gen_buffer' in checklist_generators else False,
                                 time=time_sim if time_sim != False else None)

        # TODO: duplicated code!!! Think smarter...
        store_obj: Store = warehouse.get_simulation().get_store_history()
        history = list()
        # Create a list of labels, so take only the Action name from the object "store_obj"
        for index in range(store_obj.capacity):
            history.append(store_obj.get().value)

        df = pd.DataFrame(history)

        # Take the minimum and maximum time of the simulation
        min_time_sim: Timestamp = df.min().get('Start')
        max_time_sim: Timestamp = df.max().get('Finish')
        timeline = Timeline(min_time_sim, max_time_sim)

        # Create the timeline
        fig = px.timeline(data_frame=df,
                          x_start="Start", x_end="Finish", y="Action",
                          range_x=[timeline.get_actual_left(), timeline.get_actual_right()],
                          color="Action")
        fig.update_yaxes(autorange="reversed")  # otherwise, tasks are listed from the bottom up
        # If you want a linear timeline:
        # fig.layout.xaxis.type = 'linear'
        fig.layout.xaxis.type = 'date'
        # create slider
        fig.update_xaxes(rangeslider=dict(visible=True, range=[min_time_sim, max_time_sim]))

        return fig

    # TODO: report errors
    return timeline


if __name__ == '__main__':
    app.run_server(debug=False)
