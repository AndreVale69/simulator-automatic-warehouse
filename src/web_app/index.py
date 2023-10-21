# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, ctx
from simpy import Store
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pandas import Series, Timestamp
from datetime import datetime, timedelta, date

from src.sim.warehouse import Warehouse
from collections import Counter

# TODO:
# - Priority High:
#   * Remove all garbage code
#   * Do some refactoring...
# - Priority Normal:
#   * Optimize WebPage class, including all calculates of the times inside update_graph() function


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
# prova1 = min_time_sim.time()
# prova2 = max_time_sim.time()
# prova3 = min_time_sim.date()
# prova4 = max_time_sim.date()
# prova1_delta: timedelta = timedelta(hours=prova1.hour, minutes=prova1.minute, seconds=prova1.second, microseconds=prova1.microsecond)
# prova2_delta: timedelta = timedelta(hours=prova2.hour, minutes=prova2.minute, seconds=prova2.second, microseconds=prova2.microsecond)
# diff_days: timedelta = prova4 - prova3
# diff_hours: timedelta = prova2_delta - prova1_delta

class WebPage:
    def __init__(self):
        self.left_counter: int = 0
        self.right_counter: int = 0
        self.actual_left = pd.to_datetime(min_time_sim)
        self.actual_right = self.actual_left + timedelta(minutes=1)
web_page = WebPage()

# Create the timeline
fig = px.timeline(df,
                  x_start="Start", x_end="Finish", y="Action",
                  range_x=[min_time_sim, max_time_sim])
fig.update_yaxes(autorange="reversed") # otherwise, tasks are listed from the bottom up
# If you want a linear timeline:
# fig.layout.xaxis.type = 'linear'
fig.layout.xaxis.type = 'date'
# If you want a rangeselector to zoom on each section
# See more: https://plotly.com/python/range-slider/
# fig.update_xaxes(
#     rangeslider_visible = True,
#     rangeselector = dict(
#         buttons = list([
#             dict(count = 1, label = "5m", step = "minute", stepmode = "backward"),
#             dict(count = 10, label = "10m", step = "minute", stepmode = "backward"),
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
app.layout = html.Div(children=[
    html.H1(
        children='Warehouse simulator',
        style={'textAlign': 'center'}
    ),

    dcc.Graph(
        id='graph-actions',
        figure=fig
    ),

    dcc.Download(id="download-graph"),

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
    ),

    # go to left
    dbc.Button([html.I(className='bi bi-arrow-left-circle-fill')], id='btn_left', n_clicks=0),
    # go to right
    dbc.Button([html.I(className='bi bi-arrow-right-circle-fill')], id='btn_right', n_clicks=0),
    # summary
    dbc.Button([html.I(className='bi bi-x-circle-fill'), " SUMMARY"], id='btn_summary', n_clicks=0)
])


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
    fig.write_image(f"./images/graph_actions.{extension}")
    return dcc.send_file(
        f"./images/graph_actions.{extension}"
    )

@app.callback(
    Output('graph-actions', 'figure'),
    [Input('btn_right', 'n_clicks'),
     Input('btn_left', 'n_clicks'),
     Input('btn_summary', 'n_clicks')],
    prevent_initial_call=True
)
def update_graph(clicks_right, clicks_left, clicks_summary):
    if "btn_right" == ctx.triggered_id:
        web_page.actual_left = web_page.actual_right
        web_page.actual_right += timedelta(minutes=1)
        return fig.update_xaxes(range=[web_page.actual_left,web_page.actual_right])
    if "btn_left" == ctx.triggered_id:
        web_page.actual_right = web_page.actual_left
        web_page.actual_left -= timedelta(minutes=1)
        return fig.update_xaxes(range=[web_page.actual_left, web_page.actual_right])
    if "btn_summary" == ctx.triggered_id:
        web_page.actual_left = pd.to_datetime(min_time_sim)
        web_page.actual_right = web_page.actual_left + timedelta(minutes=1)
        return fig.update_xaxes(range=[min_time_sim, max_time_sim])

if __name__ == '__main__':
    app.run_server(debug=False)
