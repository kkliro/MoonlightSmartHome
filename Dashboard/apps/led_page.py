import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

from utils import email

from utils import photoresistor

# app = dash.Dash()

led_threshold = 10.0
led_state = 0


layout = html.Div([
    html.H2(children="Lights Page"),
    
    html.P(id='led-threshold-display', children=f"Light Threshold: {led_threshold}"),
    html.P(id='resistance-state', children=f"Light Intensity: {photoresistor.get_resistance()}"),
    html.P(id='led-state', children=f"Light State: OFF"),
    
    dcc.Input(id='led-threshold-input', type='text', placeholder='Light Threshold'),
    html.Button('Update Threshold', id='led-change-threshold'),
    
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
                led_threshold = newValue
        except ValueError:   
            print("Not a float")

    return [f"Light Threshold: {led_threshold}"]

@app.callback(
    [
        Output('led-state', 'children'),
        Output('resistance-state', 'children'),
    ],
    [Input('led-interval', 'n_intervals')]
)
def on_interval_update_led(v):
    global led_state
    led_status = "OFF"
    
    if photoresistor.get_resistance() < led_threshold:
        if led_state != 1:
            email.send_email('Turning ON LED','Lower than threshold, system turned ON your LED.')
        led_state = 1
        led_status = "ON"
    else:
        if led_state != 0:
            email.send_email('Turning OFF LED','Higher than threshold, system turned OFF your LED.')
        led_state = 0
    
    photoresistor.set_led_output(led_state)

    return [f"LED State: {led_status}", f"Light Intensity: {50}"]