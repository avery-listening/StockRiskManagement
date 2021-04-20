import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from page import dev, usr


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

navbar = html.Div(
    [
        html.H2("Stock Risk Management System", className="navbar-brand"),
        dbc.Nav(
            [
                dbc.NavLink("Client Mode", href="/pages/client", active="exact"),
                dbc.NavLink("Developer Mode", href="/pages/developer", active="exact"),
            ],
            # vertical=True,
            pills=True,
        ),
    ],
    # style=SIDEBAR_STYLE,
    className="navbar"
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,

    html.Div(id='page-content', children=[])
])

home_page = dbc.Row([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("Demonstration of Stock Risk Management System"),
                        html.P(
                            [
                                "Please Select enter a mode",
                            ],
                            className="card-text",
                        ),
                    ],
                ),
                className="w-75 card text-white bg-primary mb-3",
            )],justify='center')

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/pages/developer':
        return dev.layout
    if pathname == '/pages/client':
        return usr.layout
    else:
        return home_page


if __name__ == '__main__':
    app.run_server(debug=False)