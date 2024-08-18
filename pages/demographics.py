import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from mappings import state_mapping, state_variable_mappings, population_dropdown_mappings, lifestyle_variable_mappings, health_measure_variable_mappings, demographic_variable_mappings, anthropometric_variable_mappings, chronic_condition_variable_mappings, healthcare_access_variable_mappings
from helper_functions import update_access_fig, update_anthro_fig, update_health_fig, update_chronic_fig, update_lifestyle_fig
from process_data import read_data
from app import df

register_page(__name__, name='Demographics', path='/demographics')

layout = dbc.Container(
    [
        # Top-level Dropdown for Demographic Variable Selection
        dbc.Row(
            dbc.Col(
                [
                    html.Label('Select Demographic Variable:', className='dropdown-label'),
                    dcc.Dropdown(
                        id='demographic-selector',
                        options=demographic_variable_mappings,  # Replace with your actual demographic options
                        value='age',  # Default value
                        clearable=False,
                    ),
                ],
                width=6,  # Adjust this width as necessary
                className='mb-4'
            ),
            justify='center'
        ),

        # Year Slider
        dbc.Row(
            dbc.Col(
                dcc.Slider(
                    id='year-slider',
                    min=2012,
                    max=2022,
                    step=1,
                    value=2012,
                    marks={str(year): str(year) for year in range(2012, 2023)},
                ),
                width=8,
                className='mb-4'
            ),
            justify='center'
        ),
        
        # Row for First Two Graphs
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div('Anthropometrics & Clinical Measures', className='form-label'),
                        dcc.Dropdown(
                            id='anthropometrics-selector',
                            options=anthropometric_variable_mappings,  # Replace with your actual options
                            value='bmi_category',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-anthropometrics', style={'height': '400px'}),
                        html.Div(id='explanation-anthropometrics', className='text-muted mt-2')
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.Div('Chronic Conditions', className='form-label'),
                        dcc.Dropdown(
                            id='chronic-conditions-selector',
                            options=chronic_condition_variable_mappings,  # Replace with your actual options
                            value='asthma',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-chronic-conditions', style={'height': '400px'}),
                        html.Div(id='explanation-chronic-conditions', className='text-muted mt-2')
                    ],
                    width=6
                ),
            ],
            className='mb-4'
        ),
        
        # Centered Fifth Graph
        dbc.Row(
            dbc.Col(
                [
                    html.Div('Healthcare Access', className='form-label'),
                    dcc.Dropdown(
                        id='healthcare-access-selector',
                        options=healthcare_access_variable_mappings,  # Replace with your actual options
                        value='health_insurance',  # Default value
                        clearable=False,
                        className='mb-2'
                    ),
                    dcc.Graph(id='graph-healthcare-access', style={'height': '400px'}),
                    html.Div(id='explanation-healthcare-access', className='text-muted mt-2')
                ],
                width=8,
                className='mx-auto mb-4'
            ),
        ),
        
        # Row for Last Two Graphs
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div('Health Measures', className='form-label'),
                        dcc.Dropdown(
                            id='health-measures-selector',
                            options=health_measure_variable_mappings,  # Replace with your actual options
                            value='mental_health',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-health-measures', style={'height': '400px'}),
                        html.Div(id='explanation-health-measures', className='text-muted mt-2')
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.Div('Lifestyle', className='form-label'),
                        dcc.Dropdown(
                            id='lifestyle-selector',
                            options=lifestyle_variable_mappings,  # Replace with your actual options
                            value='smoking',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-lifestyle', style={'height': '400px'}),
                        html.Div(id='explanation-lifestyle', className='text-muted mt-2')
                    ],
                    width=6
                ),
            ],
            className='mb-4'
        ),
    ],
    fluid=True
)

@callback(
    [
        Output('graph-anthropometrics', 'figure'),
        Output('graph-chronic-conditions', 'figure'),
        Output('graph-healthcare-access', 'figure'),
        Output('graph-health-measures', 'figure'),
        Output('graph-lifestyle', 'figure'),
    ],
    [
        Input('demographic-selector', 'value'),
        Input('year-slider', 'value'),
        Input('anthropometrics-selector', 'value'),
        Input('chronic-conditions-selector', 'value'),
        Input('healthcare-access-selector', 'value'),
        Input('health-measures-selector', 'value'),
        Input('lifestyle-selector', 'value')
    ],
)

def update_graphs(demographic, selected_year, anthro_var, chronic_var, access_var, health_var, lifestyle_var):
    fig_anthro = update_anthro_fig(df, selected_year, demographic, anthro_var)
    fig_chronic = update_chronic_fig(df, selected_year, demographic, chronic_var)
    fig_access = update_access_fig(df, selected_year, demographic, access_var)
    fig_health = update_health_fig(df, selected_year, demographic, health_var)
    fig_lifestyle = update_lifestyle_fig(df, selected_year, demographic, lifestyle_var)
    
    return fig_anthro, fig_chronic, fig_access, fig_health, fig_lifestyle


