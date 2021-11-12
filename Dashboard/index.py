from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import home_page, temperature_page, led_page

led_status = 0

app.layout = html.Div([
    html.H1(children='Smart Home Security'),
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            dcc.Link('Home', href='/apps/home_page'),
        ], className="row"),
        html.Div([
            dcc.Link('Temperature', href='/apps/temperature_page'),
        ], className="col"),
        html.Div([
            dcc.Link('LED', href='/apps/led_page'),
        ], className="col"),
    ], className="row"),
    html.Div(id='page-content', children=[]),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home_page':
        return home_page.layout
    elif pathname == '/apps/temperature_page':
        return temperature_page.layout
    elif pathname == '/apps/led_page':
        return led_page.layout
    else:
        return home_page.layout

if __name__ == '__main__':
    app.run_server(debug=False)