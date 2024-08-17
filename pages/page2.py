import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, register_page, callback
from dash.dependencies import Input, Output
from mappings import dtypes, state_mapping, income_bracket_midpoints, age_range_midpoints, state_variable_mappings, population_dropdown_mappings
from helper_functions import weighted_mean, weighted_median_interpolated, weighted_frequency, aggregate_weighted_frequency, aggregate_custom, get_mapping_dict, update_state_map, update_frequency_chart
from app import df

register_page(__name__, name='Summary', path='/summary')

layout = html.Div([
    html.Header(
        html.H1("Summary of Survey Data Collected", style={'text-align': 'center', 'padding': '10px'}),
    ),

    # Variable selector and Year slider
    html.Div(
        [
            html.Div(
                [
                    dcc.Slider(
                        id='year-slider-2',
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
                  [
                      dcc.Dropdown(
                          options=population_dropdown_mappings,
                          value='age',
                          placeholder='Select a variable',
                          id='variable-selector-2'
                      ),
                      html.Div(id='dd-output-container-2')
                  ]
              ),
              html.Div(
                  dcc.Graph(id='frequency-chart', style={'height': '500px'}),
                  style={'width': '48%', 'display': 'inline-block', 'padding': '20px', 'flex-grow': '1'}
              )
          ],
          style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}
      )

])

@callback(
    [Output('dd-output-container-2', 'children'),
     Output('frequency-chart', 'figure')],
    [Input('year-slider-2', 'value'),
     Input('variable-selector-2', 'value')]
)

def update_plots(selected_year, selected_variable):
    dropdown_text, frequency_chart = update_frequency_chart(selected_year, selected_variable, df)
    return dropdown_text, frequency_chart
