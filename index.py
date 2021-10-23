import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

app = dash.Dash()
fig = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = 6,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Pressure",'font': {'size': 24}},
    delta = {'reference': 380, 'increasing': {'color': "RebeccaPurple"} },
    gauge = {'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
             'steps': [
            {'range': [0, 250], 'color': 'cyan'},
            {'range': [250, 400], 'color': 'royalblue'}],
            'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 490}}))

fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})

app.layout = html.Div([
    html.H1(children='Smart Home Security'),

    html.Div(children='''
        Dashboard for Smart Security System.
    '''),

    html.Button("Change Light State", id="on-btn"),
    
    html.Div(id="output-div"),
    
    dcc.Graph(id='gauge',figure=fig),

])

@app.callback(
    [Output("output-div", "children")],
    [Input("on-btn", "n_clicks")]
)
def on_Clicked(value):
    lightOn = "Off"
    if value == None:
        raise PreventUpdate
    if value % 2 == 1:
        lightOn = "On"
    return [f"Light State: {lightOn}"]

app.run_server(debug=True)