# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, dcc, html, Input, Output, ctx
from simpy import Store
import dash_bootstrap_components as dbc
# from dash_bootstrap_templates import ThemeSwitchAIO, load_figure_template
# from datetime import datetime, timedelta, date
# import dash_daq as daq
# from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
from pandas import Timestamp

from src.sim.warehouse import Warehouse
from collections import Counter
from web_app.web_components.timeline import Timeline

# TODO:
# - Priority High:
#   * Remove all garbage code
#   * Do some refactoring...


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
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
app = Dash(external_stylesheets=[BS, dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

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
                    dbc.CardHeader(children=html.H4("Utilities", className="card-title")),

                    dbc.CardBody(
                        [
                            dbc.InputGroup([
                                # text
                                dbc.Input(id='set_step_graph', type='number', min=1,
                                          max=timeline.get_tot_tabs(), step=1, placeholder='Change view range'),
                                dbc.InputGroupText(id='info_step', children='minute/s')
                            ])
                        ]
                    ),

                    dbc.CardFooter("This is the footer"),
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(children=html.H4("Timeline of the simulation", className="card-title")),

                    dbc.CardBody(
                        [
                            dbc.Row([
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
                                ], width={"size": 'auto', "offset": 4}),
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
        ])
        ,
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
    fig.write_image(f"./images/graph_actions.{extension}", engine='kaleido', width=1920, height=1080)
    return dcc.send_file(
        f"./images/graph_actions.{extension}"
    )


@app.callback(
    Output('actual_tab', 'value'),
    [Input('btn_right', 'n_clicks'),
     Input('btn_left', 'n_clicks'),
     Input('btn_right_end', 'n_clicks'),
     Input('btn_left_end', 'n_clicks')],
    prevent_initial_call=True
)
def update_graph(clicks_right, clicks_left, clicks_right_end, clicks_left_end):
    if "btn_right" == ctx.triggered_id:
        timeline.right_btn_triggered()

    if "btn_left" == ctx.triggered_id:
        timeline.left_btn_triggered()

    if "btn_right_end" == ctx.triggered_id:
        timeline.right_end_btn_triggered()

    if "btn_left_end" == ctx.triggered_id:
        timeline.left_end_btn_triggered()

    return timeline.get_actual_tab()

@app.callback(
    Output('graph-actions', 'figure'),
    Output('actual_tab', 'invalid'),
    Output('num_tabs_graph', 'children'),
    Output('set_step_graph', 'invalid'),
    Input('btn_summary', 'n_clicks'),
    Input('actual_tab', 'value'),
    Input('set_step_graph', 'value'),
    prevent_initial_call=True
)
def update_graph(clicks_summary, val_actual_tab, val_step):
    if 'btn_summary' == ctx.triggered_id:
        return fig.update_xaxes(
            range=[timeline.get_minimum_time(),timeline.get_maximum_time()]), False, f'/{timeline.get_tot_tabs()}', False

    if 'actual_tab' == ctx.triggered_id and val_actual_tab is not None:
        timeline.set_actual_tab(val_actual_tab)
        return fig.update_xaxes(
            range=[timeline.get_actual_left(), timeline.get_actual_right()]), False, f'/{timeline.get_tot_tabs()}', False

    if 'set_step_graph' == ctx.triggered_id and val_step is not None:
        timeline.set_step(val_step)
        return fig.update_xaxes(
            range=[timeline.get_actual_left(), timeline.get_actual_right()]), False, f'/{timeline.get_tot_tabs()}', False

    if val_actual_tab is None:
        return fig.update_xaxes(
            range=[timeline.get_actual_left(), timeline.get_actual_right()]), True, f'/{timeline.get_tot_tabs()}', False

    if val_step is None:
        return fig.update_xaxes(
            range=[timeline.get_actual_left(), timeline.get_actual_right()]), False, f'/{timeline.get_tot_tabs()}', True


if __name__ == '__main__':
    app.run_server(debug=False)
