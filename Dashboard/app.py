import dash
import dash_bootstrap_components as dbc

# App Server -> creates an instance a server to be deployed on localhost
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.CYBORG], 
                )
app.title = "Moonlight Smart Home Dashboard"
server = app.server