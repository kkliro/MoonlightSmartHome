import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app import app

#from utils import led, temperature

# app = dash.Dash()

temperature = 0
humidity = 0

layout = html.Div([
    html.H2(children="Home Page"),

    html.Div(id='led-container', children=[
        html.P(id="led-status"),

        html.Button('Toggle Light', id='change-led-status'),
    ]),

    html.Div(id='temperature-container', children=[
        html.P(id='temperature-value'),
        html.P(id='humidity-value'),
    ]),

    dcc.Interval(
        id='temperature-interval',
        interval=1*1000,
        n_intervals=0
    ),
])

@app.callback(
    [
        Output('temperature-value', 'children'),
        Output('humidity-value', 'children')
    ],
    [Input('temperature-interval', 'n_intervals')]
)
def on_interval_update(v):
    #temperature = temperature.get_temp()
    #humidity = temperature.get_humidity()

    return [
        [f"Temperature: {temperature}"], 
        [f"Humidity: {humidity}"]
    ]

@app.callback(
    [Output("led-status", "children")],
    [Input("change-led-status", "n_clicks")]
)
def on_clicked(value):
    light_state = "OFF"   
    led_status = 0
    
    if (value != None):
        led_status = value % 2        

    if led_status == 1:
        light_state = "ON"

    #led.setLEDOutput(led_status)

    return [f"Light State: {light_state}"]