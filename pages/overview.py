import dash
from dash import dcc, html, callback, Input, Output, register_page
import dash_bootstrap_components as dbc
from app import df  # Assuming df is imported from a central app file
from helper_functions import update_time_series  # Import your time series function


register_page(__name__, name='Overview', path='/overview')

# Define the overview layout
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
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='variable-selector-overview',
                    options=[
                        {'label': 'Gender', 'value': 'sex'},
                        {'label': 'Age', 'value': 'age'},
                        {'label': 'Race', 'value': 'race'},
                        {'label': 'Exercise', 'value': 'exercise'},
                        {'label': 'Smoking', 'value': 'smoking'},
                        {'label': 'BMI Category', 'value': 'bmi_category'},
                        {'label': 'Asthma', 'value': 'asthma'},
                        {'label': 'Arthritis', 'value': 'arthritis'},
                        {'label': 'Cardiac Event', 'value': 'cardiac_event'},
                    ],
                    value='sex',
                    clearable=False,
                    className="mb-4"
                ),
                width=6
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='time-series-graph'),
                width=12
            ),
            className="mt-4"
        ),
    ],
    fluid=True,
    className="mt-5"
)

# Callback for the time series graph

@callback(
    Output('time-series-graph', 'figure'),
    Input('variable-selector-overview', 'value')
)
def update_time_series_graph(selected_variable):
    figure = update_time_series(df, selected_variable)
    return figure
