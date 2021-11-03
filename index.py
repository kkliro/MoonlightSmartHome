import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='My Dash'),

    html.Div(children='''
        Dash: This is my new basic Dash.
    '''),

    dcc.Graph(
        id='new-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'test1'},
           
            ],
            'layout': {
                'title': 'New Basic Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)