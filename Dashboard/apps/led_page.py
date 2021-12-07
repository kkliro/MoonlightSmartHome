import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

from utils import email_handler, led, rfid

import dash_bootstrap_components as dbc
import dash_daq as daq

light1_state = "OFF"
light2_state = "OFF"

light_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Light Reading", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.P(id='resistance-state', children=f"Light Intensity: {led.get_resistance()}"),
                html.Br(),
                html.H4("Room Light Source", className='card-text'),
                html.Br(),
                daq.Tank(
                    id='led-resistance-tank',
                    value=5,
                    min=0,
                    max=1024,
                    scale={'interval':1, 'labelInterval':150},
                    style={'margin-left': '60px'}
                ),
                html.Br(),
                html.Br(),
                html.H4("Threshold Lights Status", className='card-text'),
                html.Div(id='led-state', children=f"Light 2 State: OFF"),
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
                html.P(id='led-threshold-display', children=f"Light Threshold: {rfid.get_led_threshold()}"),
                html.P(id='led-threshold-display-hidden', children=f"Light Threshold: {rfid.get_led_threshold()}", style={'display':'none'}),
                html.Br(),
                dbc.Input(id='led-threshold-input', type='number', min=0, max=1204, placeholder='Light Threshold'),
                html.Br(),
                dbc.Button('Update Threshold', id='led-change-threshold', color="success", className="me-1"),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

led1_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Togglable Lights", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.P(f"Light State: {light1_state}", id='light1-state'),
                dbc.Row([
                    dbc.Col(html.P("Toggle Light 1: "), width='auto'),               
                    
                dbc.Col(daq.BooleanSwitch(
                    on=led.get_led_state(0),
                    id=f"toggle-light-button",
                    persistence = True,
                    color="#9B51E0",
                    ), width='auto'),
                ]),
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
        dbc.Col(led1_card, width="auto"),
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
        Output("led-threshold-display-hidden", "children"),
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
                rfid.set_led_threshold(newValue)
        except ValueError:   
            print("Not a float")

    return [f"Light Threshold: {rfid.get_led_threshold()}"]

@app.callback(
    [
        Output('led-state', 'children'),
        Output('led-resistance-tank', 'value'),
        Output('resistance-state', 'children'),
        Output("led-threshold-display", "children"),
    ],
    [Input('led-interval', 'n_intervals')]
)
def on_interval_update_led(v):
    led_status = "OFF"
    
    global light2_state
    
    try:
        if led.get_resistance() < rfid.get_led_threshold():
            if not led.get_led_state(1):
                email_handler.send_email('Turning ON LED','Lower than threshold, system turned ON your LED.')
            led.set_led_state(1, True)
            led_status = "ON"
        else:
            if led.get_led_state(1):
                email_handler.send_email('Turning OFF LED','Higher than threshold, system turned OFF your LED.')
            led.set_led_state(1, False)
    except RuntimeError as error:
        print(error.args[0])
   
    light2_state = led_status

    return [f"Light 2 State: {light2_state}", led.get_resistance(), f"Light Intensity: {led.get_resistance()}", f"Light Threshold: {rfid.get_led_threshold()}"] 

@app.callback(
    Output('light1-state', 'children'),
    Input('toggle-light-button', 'on')
)
def update_led1_output(on):
    global light1_state
    
    state = "OFF"
    if on:
        state = "ON"
    
    light1_state = state
    print(led.get_led_state(0))
    led.set_led_state(0, on)
    
    return f'Light 1 State: {light1_state}'
