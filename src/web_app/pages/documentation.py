from dash import html
from web_app.components.navbar import navbar

layout = html.Div([
    navbar,
    html.H1('Documentation'),
    html.Div('Future improvement.'),
])