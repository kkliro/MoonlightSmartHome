import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app import app

# app = dash.Dash()

layout = html.Div([
    html.H2(children="Temperature"),

    dcc.Graph(id='gauge-temp'),
    dcc.Graph(id='gauge-hum'),
    
    dcc.Interval(
        id='temperature-interval',
        interval=1*5000,
        n_intervals=0
    )
])

@app.callback(
    [
        Output('gauge-temp', 'figure'),
        Output('gauge-hum', 'figure')
    ],
    [Input('temperature-interval', 'n_intervals')]
)
def on_interval_update_graphs(v):
    temp_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 0,
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
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 29}}))

    hum_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 0,
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