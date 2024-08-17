import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, page_registry, page_container
from dash.dependencies import Input, Output
from mappings import state_mapping, income_bracket_midpoints, age_range_midpoints, dtypes
from process_data import read_data

print('Reading data...')
df = read_data(dtypes)

print('Read data.')

df['state_code'] = df['state'].map(state_mapping)

df['income_midpoint'] = df['income'].map(income_bracket_midpoints)

df['age_midpoint'] = df['age'].map(age_range_midpoints)

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1("Dashboard App"),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page['relative_path'])
        ) for page in page_registry.values()
    ]),
    page_container
])

def run_dash_app():
    app.run_server(port=8050, debug=True)

run_dash_app()