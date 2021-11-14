import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app import app

from apps import temperature_page
import dash_bootstrap_components as dbc

from utils import led, temperature, motor

import dash_daq as daq

# app = dash.Dash()

led_status = 0

g_temperature = 0
g_humidity = 0

temperature_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Temperature", className="card-title", style={'text-align':'center'}),
                daq.Gauge(
                    id='temperature-gauge-1',
                    showCurrentValue=True,
                    units="°C",
                    # color={"gradient":True,"ranges":{"blue":[-30, 10],"white":[10,22],"red":[22,30]}},
                    color='lightblue',
                    value=2,
                    size=300,
                    label=' ',
                    max=30,
                    min=-30,
                ),
                html.P("Temperature Reading", id='temperature-card-output', className="card-text", style={'font-size':'20px'}),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

humidity_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Humidity", className="card-title", style={'text-align':'center'}),
                daq.Gauge(
                    id='humidity-gauge-1',
                    showCurrentValue=True,
                    units="%",
                    # color={"gradient":True,"ranges":{"blue":[-30, 10],"white":[10,22],"red":[22,30]}},
                    color='lightgreen',
                    value=2,
                    size=300,
                    label=' ',
                    max=100,
                    min=0,
                ),
                html.P("Humidity Reading", id='humidity-card-output', className="card-text", style={'font-size':'20px'}),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

component_status_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Component States", className="card-title", style={'text-align':'center'}),
                html.H4("Lights", className='card-text'),
                dcc.Markdown("LED: ON", id='led-states-output', className="card-text", style={'font-size':'17px', "white-space": "pre"}),
                html.H4("Fan", className='card-text'),
                html.P("Fan: ON", id='fan-states-output', className="card-text", style={'font-size':'17px'}),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

cards = dbc.Row(
    [
        dbc.Col(temperature_card, width="auto"),
        dbc.Col(humidity_card, width="auto"),
        dbc.Col(component_status_card, width="auto"),
    ]
)

layout = html.Div([

    cards,

    dcc.Interval(
        id='temperature-interval',
        interval=1*1000,
        n_intervals=0
    ),
])

def get_on_or_off(value):
    if (value == 0 or not value):
        return 'off'
    else:
        return 'on'

def get_component_states():
    component_states = {
      "leds": None,
      "motor": None,
    }

    leds = led.led_light_states.copy()
    
    for i,s in enumerate(leds):
        leds[i] = get_on_or_off(leds[i])

    component_states['leds'] = leds
    component_states['motor'] = get_on_or_off(motor.motor_state)

    return component_states

@app.callback(
    [
        Output('temperature-gauge-1', 'value'),
        Output('temperature-card-output', 'children'),
        Output('humidity-gauge-1', 'value'),
        Output('humidity-card-output', 'children'),
        Output('led-states-output', 'children'),
        Output('fan-states-output', 'children'),
    ],
    [Input('temperature-interval', 'n_intervals')]
)
def on_interval_update(v):
    global g_temperature
    global g_humidity
    
    _temperature = temperature.get_temp()
    _humidity = temperature.get_humidity()

    component_states = get_component_states()
    
    if _temperature != None:
        g_temperature = _temperature
        
    if _humidity != None:
        g_humidity = _humidity

    led_states = component_states['leds']
    led_output = ""
    count = 1

    for led_state in led_states:
        led_output = led_output + f'''Light {count}: {led_state}\n'''
        count = count + 1

    current_motor_state = component_states['motor']
    motor_output = f"Fan: {current_motor_state}"

    return [
        g_temperature,
        f"Temperature: {g_temperature}°C",
        g_humidity,
        f"Humidity: {g_humidity}%",
        led_output,
        motor_output
    ]