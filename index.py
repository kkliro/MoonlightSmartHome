import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import RPi.GPIO as GPIO

import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D20)

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
LED = 23
GPIO.setup(LED, GPIO.OUT)

lastTemperature = 0
currentTemp = 0

currentHum = 0
lastHum = 0

def ConfigureLED(ledStatus):
    GPIO.output(LED, ledStatus)  
        
def GetTemp():
    try:
        global currentTemp
        global lastTemperature
        # Print the values to the serial port
        lastTemperature = currentTemp
        temperature_c = dhtDevice.temperature
        currentTemp = temperature_c
        #DisplayTemp()
        #print(currentTemp)
        #temperature_f = temperature_c * (9 / 5) + 32
        #humidity = dhtDevice.humidity
        #print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% "
        #.format(temperature_f, temperature_c, humidity))
    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        
def GetHumidity():
    try:
        global currentHum
        global lastHum
        # Print the values to the serial port
        lastHum = currentHum
        humidity = dhtDevice.humidity
        currentHum = humidity
        #DisplayTemp()
        #print(currentTemp)
        #temperature_f = temperature_c * (9 / 5) + 32
        #humidity = dhtDevice.humidity
        #print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% "
        #.format(temperature_f, temperature_c, humidity))
    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

app = dash.Dash()

app.layout = html.Div([
    html.H1(children='Smart Home Security'),

    html.Div(children='''
        Dashboard for Smart Security System.
    '''),

    html.Button("Change Light State", id="on-btn"),
    
    html.Div(id="output-div"),
    
    dcc.Graph(id='gauge-temp'),
    dcc.Graph(id='gauge-hum'),
    
    dcc.Interval(
        id='temp-interval',
        interval=1*10000,
        n_intervals=0
    ),
    
    dcc.Interval(
        id='hum-interval',
        interval=1*10000,
        n_intervals=0
    )

])

@app.callback(
    Output('gauge-temp', 'figure'),
    [Input('temp-interval', 'n_intervals')]
)
def update_graph_live_temp(n):
    GetTemp()
    #print(currentTemp)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = currentTemp,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Temperature",'font': {'size': 24}},
        delta = {'reference': lastTemperature, 'increasing': {'color': "RebeccaPurple"} },
        gauge = {'axis': {'range': [-30, 30], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "red",
                'borderwidth': 2,
                'bordercolor': "gray",
                 'steps': [
                {'range': [-30, -10], 'color': 'royalblue'},
                {'range': [-10, 10], 'color': 'white'}],
                'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 29}}))
    
    fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})
    
    return fig

@app.callback(
    Output('gauge-hum', 'figure'),
    [Input('hum-interval', 'n_intervals')]
)
def update_graph_live_hum(n):
    GetHumidity()
    #print(currentTemp)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = currentHum,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Humidity",'font': {'size': 24}},
        delta = {'reference': lastHum, 'increasing': {'color': "RebeccaPurple"} },
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
    
    fig.update_layout(paper_bgcolor = "beige", font = {'color': "darkblue", 'family': "Arial"})
    
    return fig
                

@app.callback(
    [Output("output-div", "children")],
    [Input("on-btn", "n_clicks")]
)
def on_Clicked(value):
    lightOn = "Off"
    circuitPass = 0
    
    if value == None:
        #raise PreventUpdate
        ConfigureLED(circuitPass)
        return [f"Light State: {lightOn}"]
    if value % 2 == 1:
        lightOn = "On"
        circuitPass = 1
    ConfigureLED(circuitPass)
    return [f"Light State: {lightOn}"]
    


app.run_server(debug=False)
