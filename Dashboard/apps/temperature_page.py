import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

import dash_bootstrap_components as dbc
import dash_daq as daq

from utils import email_handler, temperature, motor, rfid

# app = dash.Dash()

g_sent_email = False

temp_gauge_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Temperature Reading", className="card-title", style={'text-align':'center'}),
                html.Br(),
                dcc.Graph(id='gauge-temp'),
                html.P(id='temp-currentval-display', children=f"Current Recorded Temperature: {temperature._temperature[0]}°C"),
                html.P(id='temp-lastval-display', children=f"Last Recorded Temperature Threshold: {temperature._temperature[1]}°C"),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

humidity_gauge_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Humidity Reading", className="card-title", style={'text-align':'center'}),
                html.Br(),
                dcc.Graph(id='gauge-hum'),
                html.P(id='hum-currentval-display', children=f"Current Recorded Humidity: {temperature._humidity[0]}%"),
                html.P(id='hum-lastval-display', children=f"Last Recorded Humidity Threshold: {temperature._humidity[1]}%"),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

temp_threshold_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Temperature Threshold Settings", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.P(id='temp-threshold-display', children=f"Temperature Threshold: {rfid.get_temperature_threshold()}"),
                html.P(id='temp-threshold-display-hidden', children=f"Temperature Threshold: {rfid.get_temperature_threshold()}", style={'display':'none'}),
                html.Br(),
                dbc.Input(id='temp-threshold-input', type='number', min=-30,max=30, placeholder='Temperature Threshold'),
                html.Br(),
                dbc.Button('Update Threshold', id='temp-change-threshold', color="success", className="me-1"),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

cards = dbc.Row(
    [
        dbc.Col(humidity_gauge_card, width="auto"),
        dbc.Col(temp_gauge_card, width="auto"),
        dbc.Col(temp_threshold_card, width="auto"),
    ]
)

layout = html.Div([
    cards,
    
    dcc.Interval(
        id='temperature-interval',
        interval=1*1000, # 5 seconds
        n_intervals=0
    )
])

@app.callback(
    [
        Output("temp-threshold-display-hidden", "children"),
    ],
    [
        Input("temp-change-threshold", "n_clicks"),
    ],
    [
        State("temp-threshold-input", "value")        
    ]
)
def update_temp_threshold(n_clicks, value):
    if value != None:    
        try:
            newValue = float(value)
            if abs(newValue) <= 29 :
                rfid.set_temperature_threshold(newValue)
        except ValueError:     
            print("Not a float")

    return [f"Temperature Threshold: {rfid.get_temperature_threshold()}"]

@app.callback(
    [
        Output('gauge-temp', 'figure'),
        Output('gauge-hum', 'figure'),
        Output('temp-currentval-display', 'children'),
        Output('temp-lastval-display', 'children'),
        Output('hum-currentval-display', 'children'),
        Output('hum-lastval-display', 'children'),
        Output("temp-threshold-display", "children"),
    ],
    [Input('temperature-interval', 'n_intervals')]
)
def on_interval_update_graphs(v):
    global g_sent_email

    temperature_read = temperature.get_temp();
    humidity_read = temperature.get_humidity();
    
    if temperature_read != None:
        temperature.set_temperature(temperature_read)
        
        try:
            if temperature_read > rfid.get_temperature_threshold():
                if not g_sent_email:
                    g_sent_email = True
                    email_handler.send_email('Enable Fan', 'Would you like to turn on the fan?')
            else:
                motor.change_motor_state(False)
        except RuntimeError as error:
            print('Temperature Threshold Error')
        
    if humidity_read != None:
        temperature.set_humidity(humidity_read)
    
    #temperature_read = 20;
    #humidity_read = 50;

    email_handler.email_reader()
    
    if g_sent_email and not motor.motor_state:
        g_sent_email = True

    # elif temperature_read <= temperature_threshold:
    #     print("Send email asking to turn fan off")

    
    temp_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = temperature._temperature[0],
        domain = {'x': [0, 1], 'y': [0, 1]},
        # title = {'text': "Temperature",'font': {'size': 24}},
        delta = {'reference': temperature._temperature[1], 'increasing': {'color': "lightgreen"} },
        gauge = {'axis': {'range': [-30, 30], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "red",
                'borderwidth': 5,
                'bordercolor': "gray",
                 'steps': [
                {'range': [-30, -10], 'color': 'royalblue'},
                {'range': [-10, 10], 'color': 'white'}],
                'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': rfid.get_temperature_threshold()}}))

    hum_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = temperature._humidity[0],
        domain = {'x': [0, 1], 'y': [0, 1]},
        # title = {'text': "Humidity",'font': {'size': 24}},
        delta = {'reference': temperature._humidity[1], 'increasing': {'color': "lightgreen"} },
        gauge = {'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "red",
                'borderwidth': 2,
                'bordercolor': "gray",
                 'steps': [
                {'range': [0, 33], 'color': 'green'},
                {'range': [33, 66], 'color': 'yellow'}],
                'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 80}}))
    
    hum_fig.update_layout(paper_bgcolor = "#303030", font = {'color': "white", 'family': "Arial"})
    temp_fig.update_layout(paper_bgcolor = "#303030", font = {'color': "white", 'family': "Arial"})

    return [temp_fig, hum_fig, f"Current Recorded Temperature: {temperature._temperature[0]}°C", f"Last Recorded Temperature: {temperature._temperature[1]}°C", 
    f"Current Recorded Humidity: {temperature._humidity[0]}%", f"Last Recorded Temperature: {temperature._humidity[1]}%", f"Temperature Threshold: {rfid.get_temperature_threshold()}"]