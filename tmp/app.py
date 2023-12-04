import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, Dash

BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
app = Dash(external_stylesheets=[BS, dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           # this ensures that mobile devices don't rescale your content on small screens
           # and lets you build mobile optimised layouts
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

progress = html.Div(
    [
        dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
        dbc.Progress(id="progress"),
    ]
)

app.layout = progress


@app.callback(
    [Output("progress", "value"), Output("progress", "label")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    progress = min(n % 110, 100)
    print(progress)
    # only add text after 5% progress to ensure text isn't squashed too much
    return progress, f"{progress} %" if progress >= 5 else ""

if __name__ == "__main__":
    app.run_server(debug=True)