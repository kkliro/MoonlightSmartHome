import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


app = dash.Dash()

app.layout = html.Div([
    html.H1(children='Smart Home Security'),
])

if __name__ == '__main__':
    app.run_server(debug=True)