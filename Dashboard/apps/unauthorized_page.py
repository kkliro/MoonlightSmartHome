import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

from utils import email, led

import dash_bootstrap_components as dbc
import dash_daq as daq

layout = html.Div(style={'text-align':'center'},children=[
    html.Br(),
    html.Br(),
    html.Br(),
    html.H1(children="Unauthorized User", style={'color':'red'}),
    html.H2(children='Please scan an authorized RFID tag in order to access the dashboard\'s pages.'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H4('For more information, please contact our system admin: iotvanier.smarthome@gmail.com')
])