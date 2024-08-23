import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, register_page, callback, Input, Output
import dash_bootstrap_components as dbc

from app import df
from helper_functions import (
    weighted_mean, weighted_median_interpolated, weighted_frequency, 
    aggregate_weighted_frequency, aggregate_custom, get_mapping_dict, 
    update_state_map, update_frequency_chart, update_time_series, update_overview_bar
)
from mappings import (
    dtypes, state_mapping, income_bracket_midpoints, age_range_midpoints, 
    state_variable_mappings, population_dropdown_mappings, 
    state_fullname_mappings, demographic_variable_mappings
)

# Register the "Overview" page
register_page(__name__, name='Overview', path='/overview')

# Layout for the "Overview" page
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Container(
                    [
                        html.H2("Overview of CDC Survey Data", className="display-6"),
                        html.P(
                            "Explore key insights and high-level summaries of the CDC Survey data from 2012-2022.",
                            className="lead",
                        ),
                        html.Hr(className="my-2"),
                        html.P(
                            "This page provides an at-a-glance summary of key statistics, trends, and insights over time."
                        ),
                    ],
                    className="p-4 bg-light rounded-3"
                ),
                width=14, style={'marginBottom': '20px'}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Container(
                    [
                        html.H4("Population Breakdown By State, Variable", className="display-7"),
                        html.P(
                            "Detailed breakdown of the population by state and selected variables.",
                            className="small"
                        ),
                    ],
                    className="p-3 bg-light rounded-3"
                ),
                width=12
            )
        ),

        dbc.Row([
            dbc.Col(
                [
                    dbc.Label("Select a state:", html_for='state-selector-overview'),
                    dcc.Dropdown(
                        id='state-selector-overview',
                        options=state_fullname_mappings,
                        value=1,
                        clearable=False,
                        searchable=True,
                        className="mb-4"
                    ),
                ],
                width=6,
            ),
            dbc.Col(
                [
                    dbc.Label("Select a demographic:", html_for='demographic-selector-overview'),
                    dcc.Dropdown(
                        id='demographic-selector-overview',
                        options=demographic_variable_mappings,
                        value='age',
                        clearable=False,
                        searchable=True,
                        className="mb-4"
                    ),
                ],
                width=6
            ),]
        ),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='time-series-graph-overview'),
                width=6
            ),
            dbc.Col(
                dcc.Graph(id='stacked-bar-chart-overview'),
                width=6
            )],
            className="mt-4", style={'marginBottom': '20px'}
        ),

        dbc.Row(
            dbc.Col(
                dbc.Container(
                    [
                        html.H4("Population Breakdown By Year, Variable", className="display-7"),
                        html.P(
                            "Year-wise population breakdown based on selected variables.",
                            className="small"
                        ),
                    ],
                    className="p-3 bg-light rounded-3"
                ),
                width=12, style={'marginBottom': '20px'}
            )
        ),

    # Variable Selector and Frequency Chart with Year Slider on the right
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            options=population_dropdown_mappings,
                            value='age',
                            placeholder='Select a variable',
                            id='variable-selector-overview'
                        ),
                        html.Div(id='dd-output-container-overview')
                    ],
                    width=2,
                    className='d-flex flex-column justify-content-start'
                ),
                dbc.Col(
                    dcc.Graph(
                        id='frequency-chart-overview',
                        style={'height': '500px'},
                    ),
                    width=8,
                ),
                dbc.Col(
                    dcc.Slider(
                        id='year-slider-overview',
                        min=2012,
                        max=2022,
                        step=1,
                        value=2022,
                        marks={str(year): str(year) for year in range(2012, 2023)},
                        vertical=True,  # Make the slider vertical
                        verticalHeight=500,  # Ensure it matches the chart height
                        included=False,  # Show only the handle, not a filled bar
                        updatemode='drag',  # Update value on drag rather than release
                    ),
                    width='auto',
                    style={'padding': '10px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}  # Center the slider
                ),
            ],
            className='g-3'
        )
    ],
    fluid=True,
    className="mt-5"
)

# Callbacks for the "Overview" page
@callback(
    [
        Output('time-series-graph-overview', 'figure'),
        Output('stacked-bar-chart-overview', 'figure'),
        Output('dd-output-container-overview', 'children'),
        Output('frequency-chart-overview', 'figure'),
    ],
    [
        Input('state-selector-overview', 'value'),
        Input('demographic-selector-overview', 'value'),
        Input('year-slider-overview', 'value'),
        Input('variable-selector-overview', 'value'),
    ]
)
def update_overview(selected_state, variable, selected_year, selected_variable):
    # Update time series and bar chart figures
    time_series_figure = update_time_series(df, selected_state, variable)
    stacked_bar_figure = update_overview_bar(df, selected_state, variable)
    
    # Update frequency chart and dropdown text
    dropdown_text, frequency_chart = update_frequency_chart(selected_year, selected_variable, df)
    
    return time_series_figure, stacked_bar_figure, dropdown_text, frequency_chart
