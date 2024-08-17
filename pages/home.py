import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, register_page, callback
from dash.dependencies import Input, Output
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

register_page(__name__, name='State Map', path='/')

layout = html.Div([
    html.Header(
        html.H1("State Map", style={'text-align': 'center', 'padding': '10px'}),
    ),

    # Variable selector and Year slider
    html.Div(
        [
            html.Div(
                [
                    dcc.RadioItems(
                        id='variable-selector',
                        options=state_variable_mappings,
                        value='Average Income',
                        labelStyle={'display': 'inline-block', 'margin-right': '100px',}
                    ),
                ],
                style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}
            ),
            html.Div(
                [
                    dcc.Slider(
                        id='year-slider',
                        min=2012,
                        max=2022,
                        step=1,
                        value=2012,
                        marks={str(year): str(year) for year in range(2012, 2023)},
                    ),
                ],
                style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}
            )
        ],
        style={'display': 'flex', 'justify-content': 'center', 'flex-wrap': 'wrap'}
    ),

    # Graphs layout
    html.Div(
        [
            html.Div(
                dcc.Graph(id='choropleth-map', style={'height': '500px'}),
                style={'width': '48%', 'display': 'inline-block', 'padding': '20px','flex-grow': '1'}
            ),
        ],
        style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}
    )

])

@callback(
    [Output('choropleth-map', 'figure')],
    [Input('year-slider', 'value'),
     Input('variable-selector', 'value')]
)

def update_plots(selected_year, selected_variable):
    state_map = update_state_map(selected_year, selected_variable, df, aggregated_data)
    return [state_map]






