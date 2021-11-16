import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

from utils import email, led

import dash_bootstrap_components as dbc
import dash_daq as daq


light_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Light Readings", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.P(id='resistance-state', children=f"Light Intensity: {led.get_resistance()}"),
                html.Br(),
                html.H4("Light States", className='card-text'),
                html.Div(id='led-state', children=f"Light State: OFF"),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

light_threshold_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Light Threshold Settings", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.P(id='led-threshold-display', children=f"Light Threshold: {led.led_threshold}"),
                html.Br(),
                dbc.Input(id='led-threshold-input', type='text', placeholder='Light Threshold'),
                html.Br(),
                dbc.Button('Update Threshold', id='led-change-threshold', color="success", className="me-1"),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

cards = dbc.Row(
    [
        dbc.Col(light_card, width="auto"),
        dbc.Col(light_threshold_card, width="auto"),
    ]
)

layout = html.Div([
    # html.H2(children="Lights Page"),

    cards,
    
    dcc.Interval(
        id='led-interval',
        interval=1*1000, 
        n_intervals=0
    )
    
])

@app.callback(
    [
        Output("led-threshold-display", "children"),
    ],
    [
        Input("led-change-threshold", "n_clicks"),
    ],
    [
        State("led-threshold-input", "value")        
    ]
)
def update_led_threshold(n_clicks, value):
    global led_threshold
    
    if value != None:    
        try:
            newValue = float(value)
            if abs(newValue) >= 0:
                led.set_led_threshold(newValue)
        except ValueError:   
            print("Not a float")

    return [f"Light Threshold: {led.led_threshold}"]

@app.callback(
    [
        Output('led-state', 'children'),
        Output('resistance-state', 'children'),
    ],
    [Input('led-interval', 'n_intervals')]
)
def on_interval_update_led(v):
    led_status = "OFF"
    
    if led.get_resistance() < led.led_threshold:
        if not led.get_led_state(1):
            email.send_email('Turning ON LED','Lower than threshold, system turned ON your LED.')
        led.set_led_state(1, True)
        led_status = "ON"
    else:
        if led.get_led_state(1):
            email.send_email('Turning OFF LED','Higher than threshold, system turned OFF your LED.')
        led.set_led_state(1, False)
    
    # led.set_led_output(1, led_state)

    p_elements = []

    count = 1
    for state in led.led_light_states:
        is_on = False

        p_text = f"Light {count}: "
        if not state:
            p_text = p_text + "off"
        else:
            is_on = True
            p_text = p_text + "on"

        p_elements.append(html.Div(children=[
            dbc.Row([
                dbc.Col(p_text, width='auto'),               
                
                dbc.Col(daq.BooleanSwitch(
                    on=is_on,
                    id=f"light-switch-{count}",
                    color="#9B51E0",
                ), width='auto'),
            ]),
            html.Br()
        ]))

        count = count + 1

    return [p_elements, f"Light Intensity: {led.get_resistance()}"] 
