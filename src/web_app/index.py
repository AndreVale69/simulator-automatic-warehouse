# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from src.sim.warehouse import Warehouse
from collections import Counter

warehouse = Warehouse()
warehouse.run_simulation()
cn = Counter(warehouse.get_events_to_simulate())

BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
app = Dash(external_stylesheets=[BS])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Actions": ["Send back a drawer", "Extract a drawer", "Insert material", "Remove material"],
    "Nums Executions": [cn.get("send_back"), cn.get("extract_drawer"), cn.get("ins_mat"), cn.get("rmv_mat")]
})

fig = px.bar(df, x="Actions", y="Nums Executions", barmode="stack",
             title='Number of actions performed', color='Actions')

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
                    "SVG", id="dropdown-btn_svg", n_clicks=0
                ),
                dbc.DropdownMenuItem(
                    "PDF", id="dropdown-btn_pdf", n_clicks=0
                )
            ],
            label="Download Graph",
    ),
    dcc.Download(id="download-svg"),
    dcc.Download(id="download-pdf")

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
    # which button is triggered
    if "dropdown-btn_svg" == ctx.triggered_id:
        extension = 'svg'
    elif "dropdown-btn_pdf" == ctx.triggered_id:
        extension = 'pdf'
    # take graph to download
    fig.write_image(f"./images/graph_actions.{extension}")
    return dcc.send_file(
        f"./images/graph_actions.{extension}"
    )


# fig.to_image(format="svg", engine="kaleido")

if __name__ == '__main__':
    app.run_server(debug=False)
