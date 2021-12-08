import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

import dash_bootstrap_components as dbc
import dash_daq as daq

from utils import rfid, read_bluetooth_devices

# Last saved bluetooth reading
last_content = html.Div(children=[  
    html.Br(),
    html.Div(children=dbc.Table(html.Thead(html.Tr([html.Th("Device ID"), html.Th("RSSI")])), bordered=True))  
])

# Widget to display list of devices
bluetooth_details_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Bluetooth Device Detection", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.Div(children=[
                    html.P(id='last-check-time-bt', children=[f'Last Check: {read_bluetooth_devices.get_last_checked_time()}']),
                ]),
                html.Div(id='bt-check-results', children=last_content),
            ]
        ),
    ],
    style={"width": "30rem"},
)

# Widget displaying threshold settings
bluetooth_threshold_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Bluetooth Threshold Settings", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.P(id='bt-threshold-display', children=f"RSSI Threshold: {rfid.get_rssi_threshold()}"),
                html.P(id='bt-threshold-display-hidden', children=f"RSSI Threshold: {rfid.get_rssi_threshold()}", style={'display':'none'}),
                html.Br(),
                dbc.Input(id='bt-threshold-input', type='number', min=0,max=255, placeholder='RSSI Threshold'),
                html.Br(),
                dbc.Button('Update Threshold', id='bt-change-threshold', color="success", className="me-1"),
            ]
        ),
    ],
    style={"width": "30rem"},
)

cards = dbc.Row(
    [
        dbc.Col(bluetooth_details_card, width="auto"),
        dbc.Col(bluetooth_threshold_card, width="auto"),
    ]
)

# Bluetooth page layout
layout = html.Div([
    cards,
    
    dcc.Interval(
        id='bt-interval',
        interval=1*1000, # 1 seconds
        n_intervals=0
    ),
    
    dcc.Interval(
        id='bt-check-interval',
        interval=1*30000, # 1 seconds
        n_intervals=0
    )
])

# Called whenever button is clicked to update threshold
@app.callback(
    [
        Output("bt-threshold-display-hidden", "children"),
    ],
    [
        Input("bt-change-threshold", "n_clicks"),
    ],
    [
        State("bt-threshold-input", "value")        
    ]
)
def update_bt_threshold(n_clicks, value):
    if value != None:    
        try:
            newValue = float(value)
            if abs(newValue) <= 255 :
                rfid.set_rssi_threshold(newValue)
        except ValueError:     
            print("Not a float")

    return [f"RSSI Threshold: {rfid.get_rssi_threshold()}"]

# Called every interval 
@app.callback(
    [
        Output("bt-threshold-display", "children"),
    ],
    [Input('bt-interval', 'n_intervals')]
)
def on_interval_update_bt_displays(v):
   return [f"RSSI Threshold: {rfid.get_rssi_threshold()}"]

# Called every interval to update bluetooth devices
@app.callback(
    [
        Output("bt-check-results", "children"),
        Output("last-check-time-bt", "children"),
    ],
    [
        Input("bt-check-interval", "n_intervals"),
    ],
)
def update_nearby_devices(n_intervals):
    global last_content
    
    if not rfid.is_authorized():
        raise PreventUpdate
    
    device_information = read_bluetooth_devices.scan_devices()
    device_details = device_information['details']
    
    print(f'Device Info: {device_information}')
    
    details_rows = []
    
    num_below = 0
    
    if device_information['device_count'] > 0:  
        for device in device_details:
            device_id = device
            rssi = device_details[device_id]
            
            if float(rssi) >= rfid.get_rssi_threshold():
                row = html.Tr([html.Td(device_id), html.Td(rssi)])
                details_rows.append(row)
            else:
                num_below = num_below + 1
    
    number_of_devices = int(device_information['device_count']) - num_below
    
    table_header = [
        html.Thead(html.Tr([html.Th("Device ID"), html.Th("RSSI")]))
    ]
    table_body = [html.Tbody(details_rows)]

    table = dbc.Table(table_header + table_body, bordered=True)
    
    content = html.Div(children=[
        html.Br(),
        html.P(f"Number of Nearby Devices: {number_of_devices}"),
        html.Br(),
        html.Div(children=table)
    ])
    
    last_content = content

    return [last_content, f"Last Checked: {read_bluetooth_devices.get_last_checked_time()}"]

