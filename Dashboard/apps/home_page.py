import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app import app

from utils import led

# app = dash.Dash()

layout = html.Div([
    html.H2(children="Home Page"),

    html.P(id="led-status"),

    html.Button('Toggle Light', id='change-led-status'),

    # dcc.Interval(
    #     id='led-interval',
    #     interval=1*500,
    #     n_intervals=0
    # ),
])

# @app.callback(
#     [Output('led-status', 'children')],
#     [Input('led-interval', 'n_intervals')]
# )
# def update_status(v):
#     lightState = "OFF"
#     if (led_status == 1):
#         lightState = "ON"
#     return [f"Light State: {lightState}"]

@app.callback(
    [Output("led-status", "children")],
    [Input("change-led-status", "n_clicks")]
)
def on_Clicked(value):
    light_state = "OFF"   
    led_status = 0
    
    if (value != None):
        led_status = value % 2        

    if led_status == 1:
        light_state = "ON"

    #led.setLEDOutput(led_status)

    return [f"Light State: {light_state}"]