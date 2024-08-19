import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from mappings import dtypes, state_mapping, income_bracket_midpoints, age_range_midpoints, state_variable_mappings, population_dropdown_mappings
from helper_functions import weighted_mean, weighted_median_interpolated, weighted_frequency, aggregate_weighted_frequency, aggregate_custom, get_mapping_dict, update_state_map, update_frequency_chart
from app import df

register_page(__name__, name='Summary', path='/summary')

layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Summary of Survey Data Collected", 
                    style={'text-align': 'center', 'padding': '10px'}
                ),
                width=12
            ),
            className='mb-4'
        ),

        # Year Slider
        dbc.Row(
            dbc.Col(
                dcc.Slider(
                    id='year-slider-2',
                    min=2012,
                    max=2022,
                    step=1,
                    value=2022,
                    marks={str(year): str(year) for year in range(2012, 2023)},
                ),
                width=8,
            ),
            className='justify-content-center mb-4',
        ),

        # Variable Selector and Frequency Chart
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            options=population_dropdown_mappings,
                            value='age',
                            placeholder='Select a variable',
                            id='variable-selector-2'
                        ),
                        html.Div(id='dd-output-container-2')
                    ],
                    width=2,
                ),
                dbc.Col(
                    dcc.Graph(
                        id='frequency-chart',
                        style={'height': '500px'},
                    ),
                    width=8,
                )
            ],
            className='align-items-center g-3'
        ),
    ],
    fluid=True
)


@callback(
    [Output('dd-output-container-2', 'children'),
     Output('frequency-chart', 'figure')],
    [Input('year-slider-2', 'value'),
     Input('variable-selector-2', 'value')]
)

def update_plots(selected_year, selected_variable):
    dropdown_text, frequency_chart = update_frequency_chart(selected_year, selected_variable, df)
    return dropdown_text, frequency_chart
