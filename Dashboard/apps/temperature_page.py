import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app import app

from utils import email

#from utils import temperature

# app = dash.Dash()

temperature_threshold = 25.0

layout = html.Div([
    html.H2(children="Temperature"),
    
    html.P(id='threshold-display', children=f"Temperature Threshold: {temperature_threshold}"),
    
    dcc.Input(id='threshold-input', type='text', placeholder='Temperature Threshold'),
    #html.Button('Update Threshold', id='change-threshold'),
    

    dcc.Graph(id='gauge-temp'),
    dcc.Graph(id='gauge-hum'),
    
    dcc.Interval(
        id='temperature-interval',
        interval=1*5000, # 5 seconds
        n_intervals=0
    )
])

@app.callback(
    [
        Output("threshold-display", "children"),
    ],
    [
        #Input("change-threshold", "n_clicks"),
        Input("threshold-input", "value"), 
    ]
)
def update_threshold(value):
    global temperature_threshold
    
    if value != None:    
        try:
            newValue = float(value)
            if abs(newValue) <= 30 :
                temperature_threshold = newValue
        except ValueError:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print("Not a float")

    return [f"Temperature Threshold: {temperature_threshold}"]

@app.callback(
    [
        Output('gauge-temp', 'figure'),
        Output('gauge-hum', 'figure')
    ],
    [Input('temperature-interval', 'n_intervals')]
)
def on_interval_update_graphs(v):
    #temperature_read = temperature.get_temp();
    #humidity_read = temperature.get_humidity();
    temperature_read = 20;
    humidity_read = 50;

    email.email_reader()

    if temperature_read > temperature_threshold:
        email.send_email('Enable Fan', 'Would you like to turn on the fan?')

    # elif temperature_read <= temperature_threshold:
    #     print("Send email asking to turn fan off")

    
    temp_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = temperature_read,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Temperature",'font': {'size': 24}},
        delta = {'reference': 0, 'increasing': {'color': "RebeccaPurple"} },
        gauge = {'axis': {'range': [-30, 30], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "red",
                'borderwidth': 2,
                'bordercolor': "gray",
                 'steps': [
                {'range': [-30, -10], 'color': 'royalblue'},
                {'range': [-10, 10], 'color': 'white'}],
                'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 0.75,
                'value': temperature_threshold}}))

    hum_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = humidity_read,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Humidity",'font': {'size': 24}},
        delta = {'reference': 0, 'increasing': {'color': "RebeccaPurple"} },
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
                'value': 99}}))
    
    hum_fig.update_layout(paper_bgcolor = "beige", font = {'color': "darkblue", 'family': "Arial"})
    temp_fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})

    return [temp_fig, hum_fig]