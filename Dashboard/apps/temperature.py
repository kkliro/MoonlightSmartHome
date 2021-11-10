import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# app = dash.Dash()

layout = html.Div([
    html.H2(children="Temperature"),
])

# if __name__ == '__main__':
#     app.run_server(debug=True)