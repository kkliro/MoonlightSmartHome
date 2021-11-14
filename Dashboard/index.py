from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

import dash_bootstrap_components as dbc

# Connect to your app pages
from apps import home_page, temperature_page, led_page

led_status = 0

# styling the sidebar
PAGE_STYLE = {
    # "position": "fixed",
    # "top": 0,
    # "left": 0,
    # "bottom": 0,
    # "width": "16rem",
    "padding": "2rem 1rem",
    # "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Smart Home Dashboard", className="display-4"),
        html.H4("Current User: Konstantin K."),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/apps/home_page", active="exact"),
                dbc.NavLink("Temperature & Humidity", href="/apps/temperature_page", active="exact"),
                dbc.NavLink("Lights", href="/apps/led_page", active="exact"),
            ],
            horizontal=True,
            pills=True,
        ),
        html.Hr(),
    ],
    style=PAGE_STYLE,
)

app.layout = html.Div(children=[
    sidebar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[], style=PAGE_STYLE),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home_page':
        return home_page.layout
    elif pathname == '/apps/temperature_page':
        return temperature_page.layout
    elif pathname == '/apps/led_page':
        return led_page.layout
    else:
        return home_page.layout

if __name__ == '__main__':
    app.run_server(debug=True)