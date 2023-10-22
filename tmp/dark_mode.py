from dash import Dash, html, Input, Output, State, callback
import dash_daq as daq

app = Dash(__name__)

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

rootLayout = html.Div([
    daq.Thermometer(
        min=95,
        max=105,
        value=98.6,
        id='darktheme-daq-thermometer',
        className='dark-theme-control'
    ), html.Br()
])

app.layout = html.Div(id='dark-theme-container', children=[
    daq.ToggleSwitch(
        id='toggle-theme',
        label=['Light', 'Dark'],
        value=True
    ),
    html.Br(),
    html.Div(id='dark-theme-components-1', children=[
        daq.DarkThemeProvider(theme=theme, children=rootLayout)
    ], style={
        'border': 'solid 1px #A2B1C6',
        'border-radius': '5px',
        'padding': '50px',
        'margin-top': '20px'
    })
], style={'padding': '50px'})


@callback(
    Output('dark-theme-components-1', 'children'),
    Input('toggle-theme', 'value')
)
def edit_theme(dark):

    if(dark):
        theme.update(dark=True)
    else:
        theme.update(dark=False)
    return daq.DarkThemeProvider(theme=theme, children=rootLayout)

@callback(
    Output('dark-theme-components-1', 'style'),
    Input('toggle-theme', 'value'),
    State('dark-theme-components-1', 'style')
)
def switch_bg(dark, currentStyle):
    if(dark):
        currentStyle.update(backgroundColor='#303030')
    else:
        currentStyle.update(backgroundColor='white')
    return currentStyle

if __name__ == '__main__':
    app.run(debug=True)
