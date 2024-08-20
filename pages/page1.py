import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# from pyngrok import ngrok
from mappings import dtypes, state_mapping, income_bracket_midpoints, age_range_midpoints, state_variable_mappings, population_dropdown_mappings
from helper_functions import weighted_mean, weighted_median_interpolated, weighted_frequency, aggregate_weighted_frequency, aggregate_custom, get_mapping_dict, update_state_map, update_frequency_chart
from process_data import read_data

from app import df

# Aggregate data for continuous variables
print('Aggregating data...')
aggregated_data = {
    'income': aggregate_custom(
        df, groupby_cols=['year', 'state_code'], value_col='income_midpoint', result_col_name='Average Income', agg_func=weighted_mean
    ),
    'height': aggregate_custom(
        df, groupby_cols=['year', 'state_code'], value_col='height', result_col_name='Average Height', agg_func=weighted_mean
    ),
    'weight': aggregate_custom(
        df, groupby_cols=['year', 'state_code'], value_col='weight', result_col_name='Average Weight', agg_func=weighted_mean, scale_factor=100
    ),
    'age': aggregate_custom(
        df, groupby_cols=['year', 'state_code'], value_col='age_midpoint', result_col_name='Average Age', agg_func=weighted_mean
    )
}
print('Finished aggregating data.')

register_page(__name__, name='State Map', path='/statemap')

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div('Select variable:', className='dropdown-label'),
                    width=1
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='variable-selector-state-map',
                        options=state_variable_mappings,
                        value='Average Income',
                    ),
                    width=2
                ),
                dbc.Col(
                    html.Div('Select year:', className='form-label'),
                ),
                dbc.Col(
                    dcc.Slider(
                        id='year-slider-state-map',
                        min=2012,
                        max=2022,
                        step=1,
                        value=2022,
                        marks={str(year): str(year) for year in range(2012, 2023)},
                    ),
                    width=10,
                ),
            ],
            className='align-items-center g-3',
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='choropleth-map-state-map',
                        style={'height': '500px'},
                    ),
                    width=8
                )
            ],
            className='mb-4'
        )
    ],
    fluid=True
)

@callback(
    [Output('choropleth-map-state-map', 'figure')],
    [Input('year-slider-state-map', 'value'),
     Input('variable-selector-state-map', 'value')]
)

def update_plots(selected_year, selected_variable):
    state_map = update_state_map(selected_year, selected_variable, df, aggregated_data)
    return [state_map]






