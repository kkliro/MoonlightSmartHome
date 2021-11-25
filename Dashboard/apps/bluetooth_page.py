import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

import dash_bootstrap_components as dbc
import dash_daq as daq

from utils import rfid, bluetooth_handler

last_content = html.Div()

bluetooth_details_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Bluetooth Device Detection", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.Div(children=[
                    dbc.Row(
                        [
                            dbc.Col(dbc.Button('Find Nearby Devices', id='bt-find-btn', color="success", className="me-1"), width="auto"),
                            dbc.Col(html.P(id='last-check-time-bt', children=[f'Last Check: {bluetooth_handler.get_last_checked_time()}']), width="auto"),
                        ]),
                ]),
                html.Div(id='bt-check-results', children=last_content),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

bluetooth_threshold_card = dbc.Card(
    [
        # dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("Bluetooth Threshold Settings", className="card-title", style={'text-align':'center'}),
                html.Br(),
                html.P(id='bt-threshold-display', children=f"RSSI Threshold: {rfid.get_rssi_threshold()}"),
                html.P(id='bt-threshold-display-hidden', children=f"Temperature Threshold: {rfid.get_rssi_threshold()}", style={'display':'none'}),
                html.Br(),
                dbc.Input(id='bt-threshold-input', type='number', min=0,max=255, placeholder='RSSI Threshold'),
                html.Br(),
                dbc.Button('Update Threshold', id='bt-change-threshold', color="success", className="me-1"),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "30rem"},
)

cards = dbc.Row(
    [
        dbc.Col(bluetooth_threshold_card, width="auto"),
        dbc.Col(bluetooth_details_card, width="auto"),
    ]
)

layout = html.Div([
    cards,
    
    dcc.Interval(
        id='bt-interval',
        interval=1*1000, # 1 seconds
        n_intervals=0
    )
])

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

@app.callback(
    [
        Output("bt-threshold-display", "children"),
    ],
    [Input('bt-interval', 'n_intervals')]
)
def on_interval_update_bt_displays(v):
   return [f"RSSI Threshold: {rfid.get_rssi_threshold()}"]

@app.callback(
    [
        Output("bt-check-results", "children"),
        Output("last-check-time-bt", "children"),
    ],
    [
        Input("bt-find-btn", "n_clicks"),
    ],
)
def update_nearby_devices(n_clicks):
    global last_content
    
    if n_clicks == None:
        return [last_content, f"Last Checked: {bluetooth_handler.get_last_checked_time()}"]
    
    device_information = bluetooth_handler.get_connected_devices_info()
    device_details = device_information['details']
    
    details_rows = []
    
    num_below = 0
    
    if device_information['device_count'] > 0:  
        for device in device_details:
            name = device_details[device]['name']
            rssi = device_details[device]['rssi']
            addr = device_details[device]['addr']
            
            if float(rssi) >= rfid.get_rssi_threshold():
                row = html.Tr([html.Td(name), html.Td(addr), html.Td(rssi)])
                details_rows.append(row)
            else:
                num_below = num_below + 1
    
    number_of_devices = int(device_information['device_count']) - num_below
    
    table_header = [
        html.Thead(html.Tr([html.Th("Device Name"), html.Th("Device Address"), html.Th("RSSI")]))
    ]
    table_body = [html.Tbody(details_rows)]

    table = dbc.Table(table_header + table_body, bordered=True)
    
    content = html.Div(children=[
        html.Br(),
        html.P(f"Number of Nearby Devices: {number_of_devices}"),
        html.Br(),
        html.Div(children=table)
    ])
    
    print(bluetooth_handler.get_last_checked_time())
    
    last_content = content

    return [last_content, f"Last Checked: {bluetooth_handler.get_last_checked_time()}"]

