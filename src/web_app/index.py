# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import datetime

from src.sim.warehouse import Warehouse
from collections import Counter

# Initialize the Warehouse for simulation
warehouse = Warehouse()
warehouse.run_simulation()
cn = Counter(warehouse.get_events_to_simulate())

# Import bootstrap components
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
app = Dash(external_stylesheets=[BS, dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


"""
    #########################
    * Set-up all components *
    #########################
"""
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Actions": ["Send back a drawer", "Extract a drawer", "Insert material", "Remove material"],
#     "Nums Executions": [cn.get("send_back"), cn.get("extract_drawer"), cn.get("ins_mat"), cn.get("rmv_mat")]
# })

#fig = px.bar(df, x="Actions", y="Nums Executions", barmode="stack",
#             title='Number of actions performed', color='Actions')

#prova = [
#    dict(Action="Job A", Start='2009-01-01', Finish='2009-02-28'),
#    dict(Action="Job B", Start='2009-03-05', Finish='2009-04-15'),
#    dict(Action="Job C", Start='2009-02-20', Finish='2009-05-30')
#]
#prova.append(dict(Action="Job D", Start='2009-02-20', Finish='2009-05-30'))

store_obj = warehouse.get_simulation().get_store_history()
history = []
for info in range(store_obj.capacity):
    history.append(store_obj.get().value)

df = pd.DataFrame(history)

from pandas import Series
prova:Series = df.min()
prova2:Series = df.max()
prova3:datetime = datetime.datetime.now()

fig = px.timeline(df,
                  x_start="Start", x_end="Finish", y="Action",
                  range_x=[prova.get('Start'), prova2.get('Finish')])
fig.update_yaxes(autorange="reversed") # otherwise, tasks are listed from the bottom up
# if you want a linear timeline:
# fig.layout.xaxis.type = 'linear'
fig.layout.xaxis.type = 'date'
# fig.update_xaxes(range=[prova.get('Start'), prova2.get('Finish')])
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
        style={
            'textAlign': 'center',
        }
    ),

    # html.Div(children='How many actions have been performed.', style={
    #     'textAlign': 'center',
    # }),

    dcc.Graph(
        id='graph-actions',
        figure=fig
    ),

    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(
                [html.I(className='bi bi-download'), " SVG"], id="dropdown-btn_svg", n_clicks=0
            ),
            dbc.DropdownMenuItem(
                [html.I(className='bi bi-download'), " PDF"], id="dropdown-btn_pdf", n_clicks=0
            )
        ],
        label="Download Graph"
    ),

    dbc.Button([html.I(className='bi bi-arrow-right-circle-fill')], id='btn', n_clicks=0)
    #dcc.Download(id="download-svg"),
    #dcc.Download(id="download-pdf")

    # html.Div([
    #     dbc.Button("Download Graph as SVG", id="btn_svg", color="primary"),
    #     dcc.Download(id="download-svg"),

    #     dbc.Button("Download Graph as PDF", id="btn_pdf"),
    #     dcc.Download(id="download-pdf")
    # ], className="d-grid gap-2 col-6 mx-auto")

])


@app.callback(
    Output("download-svg", "data"),
    Input("dropdown-btn_svg", "n_clicks"),
    Input("dropdown-btn_pdf", "n_clicks"),
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
    [Input('btn', 'n_clicks')],
    prevent_initial_call=True
)
def update_graph(n_clicks):
    return fig.update_xaxes(range=[prova.get('Start'), prova3])


if __name__ == '__main__':
    app.run_server(debug=False)
