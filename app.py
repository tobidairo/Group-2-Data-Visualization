import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, page_registry, page_container
from dash.dependencies import Input, Output
from mappings import state_mapping, income_bracket_midpoints, age_range_midpoints, dtypes
from process_data import read_data
import dash_bootstrap_components as dbc

print('Reading data...')
df = read_data(dtypes)

print('Read data.')

df['state_code'] = df['state'].map(state_mapping)

df['income_midpoint'] = df['income'].map(income_bracket_midpoints)

df['age_midpoint'] = df['age'].map(age_range_midpoints)

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE])

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Survey Dashboard", href="/"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("State Map", href="/")),
                    dbc.NavItem(dbc.NavLink("Summary", href="/summary")),
                    dbc.NavItem(dbc.NavLink("Demographics", href="/demographics")),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("More", header=True),
                            dbc.DropdownMenuItem("User Guide", href="/user-guide"),
                            dbc.DropdownMenuItem("About", href="/about"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="More",
                    ),
                ],
                className="ml-auto",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    sticky="top",
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                dbc.Button("Home", href='/', color='primary', className='mr-2'),
                align='left',
                width='auto'
            ),
            dbc.Col(
                dbc.Button("Back to Top", href='#', color='secondary', className='mr-2'),
                align='center',
                width='auto'
            ),
            dbc.Col(
                html.A("GitHub", href='/'),
                align='right',
                width='auto'
            )
        ],
        justify='between'  # Space out columns evenly
    ),
    className='footer',
    fluid=True
)

app.layout = html.Div([
    navbar,
    page_container,
    footer,
])

def run_dash_app():
    app.run_server(port=8050, debug=True)

run_dash_app()