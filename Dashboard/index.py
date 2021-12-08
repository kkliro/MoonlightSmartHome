from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Connect to main app.py file
from app import app
from app import server

import dash_bootstrap_components as dbc

from utils import rfid, mqtt_server

# Connect to your app pages
from apps import home_page, temperature_page, led_page, unauthorized_page, bluetooth_page

page_was_denied = True

# Sidebar styling
PAGE_STYLE = {
    "padding": "2rem 1rem",
}

# Padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Sidebar HTML structure
sidebar = html.Div(id='index-sidebar',
    children=[
        html.H2("Moonlight Smart Home", className="display-4"),
        html.H4(id='profile-name', children="Current User: Konstantin K."),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/apps/home_page", active="exact"),
                dbc.NavLink("Temperature & Humidity", href="/apps/temperature_page", active="exact"),
                dbc.NavLink("Lights", href="/apps/led_page", active="exact"),
                dbc.NavLink("Bluetooth Devices", href="/apps/bluetooth_page", active="exact"),
            ],
            horizontal=True,
            pills=True,
        ),
        html.Hr(),
    ],
    style={'display':'block'},
)

# Default application layout when dashboard is first loaded
app.layout = html.Div(children=[
    sidebar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[], style=PAGE_STYLE),
    html.Div(id='rfid-check-display', style={'display':'none'}),
    dcc.Interval(
        id='rfid-check-interval',
        interval=1*1000,
        n_intervals=0
    ),
    
    dcc.Interval(
        id='rfid-name-interval',
        interval=1*1000,
        n_intervals=0
    ),
])

# Callback whenever the rfid-name-interval is triggered, to display login name
@app.callback([
        Output('profile-name', 'children')
    ],
    [Input('rfid-check-interval', 'n_intervals')])
def on_update_rfid_name(v):
    return [f"Current User: {rfid.get_profile_name()}"]

# Callback whenever the rfid-check-display is triggered, to display unauthorized page if user is denied
@app.callback([
        Output('rfid-check-display', 'children'),
        Output('url', 'pathname'),       
    ],
    [Input('rfid-check-interval', 'n_intervals')])
def on_check_rfid_interval(v):
    global page_was_denied
    
    name = rfid.check_for_scanned_tag()
    
    allowed = rfid.is_authorized()
    
    if allowed and not page_was_denied:
        raise PreventUpdate
    
    page_was_denied = not allowed 
        
    return ["Text", "/apps/home_page"]

# Callback whenever a hyperlink is pressed, nagivates through the application pages
@app.callback([
                Output('page-content', 'children'),
                Output('index-sidebar', 'style'),
                ],
              [Input('url', 'pathname')])
def display_page(pathname):
    sidebar_display_style = 'block'
    new_layout = unauthorized_page.layout

    if not rfid.is_authorized():
        sidebar_display_style = 'none'
        new_layout = unauthorized_page.layout 
    else:
        layout_elements = None
        if pathname == '/apps/home_page':
            # return home_page.layout
            new_layout = html.Div(children=[
                html.Div(home_page.layout, style={'display':'block'}),
                html.Div(temperature_page.layout, style={'display':'none'}),
                html.Div(led_page.layout, style={'display':'none'}),
                html.Div(bluetooth_page.layout, style={'display':'none'}),
            ])
        if pathname == '/apps/temperature_page':
            new_layout = html.Div(children=[
                html.Div(home_page.layout, style={'display':'none'}),
                html.Div(temperature_page.layout, style={'display':'block'}),
                html.Div(led_page.layout, style={'display':'none'}),
                html.Div(bluetooth_page.layout, style={'display':'none'}),
            ])
        elif pathname == '/apps/led_page':
            new_layout = html.Div(children=[
                html.Div(home_page.layout, style={'display':'none'}),
                html.Div(temperature_page.layout, style={'display':'none'}),
                html.Div(led_page.layout, style={'display':'block'}),
                html.Div(bluetooth_page.layout, style={'display':'none'}),
            ])
        elif pathname == '/apps/bluetooth_page':
            new_layout = html.Div(children=[
                html.Div(home_page.layout, style={'display':'none'}),
                html.Div(temperature_page.layout, style={'display':'none'}),
                html.Div(led_page.layout, style={'display':'none'}),
                html.Div(bluetooth_page.layout, style={'display':'block'}),
            ])
        else:
            new_layout = html.Div(children=[
                html.Div(home_page.layout, style={'display':'block'}),
                html.Div(temperature_page.layout, style={'display':'none'}),
                html.Div(led_page.layout, style={'display':'none'}),
                html.Div(bluetooth_page.layout, style={'display':'none'}),
            ])

    return [new_layout, {'display':sidebar_display_style}]

if __name__ == '__main__':
    app.run_server(debug=False)