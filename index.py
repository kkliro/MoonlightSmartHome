import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Smart Home Security'),

    html.Div(children='''
        Dashboard for Smart Security System.
    '''),

    html.Button("ON", id="on-btn"),    

    html.Div(id="output-div"),

    dcc.Graph(
        id='temp-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'test1'},
           
            ],
            'layout': {
                'title': 'Temperature Recording'
            }
        }
    )
])

@app.callback(
    [Output("output-div", "children")],
    [Input("on-btn", "n_clicks")]
)
def on_Clicked(value):
    if value == None:
        raise PreventUpdate
    return [f"You clicked {value} times"]

if __name__ == '__main__':
    app.run_server(debug=True)