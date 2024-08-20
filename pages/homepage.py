import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html, register_page, callback
import dash_bootstrap_components as dbc
from app import df

register_page(__name__, name='Homepage', path='/')

# Define the homepage layout
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Container(
                    [
                        html.H1("Welcome to the CDC Survey Dashboard", className="display-4"),
                        html.P(
                            "This dashboard provides insights and visualizations from the CDC Survey Data"
                            "across various demographics and lifestyle categories, from 2012-2022.",
                            className="lead",
                        ),
                        html.Hr(className="my-2"),
                        html.P(
                            "Use the navigation bar to explore detailed maps, summaries, and insights."
                        ),
                        dbc.Button("Get Started", color="primary", href="/summary"),
                    ],
                    className="p-5 bg-light rounded-3"
                ),
                width=12
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Interactive State Map", className="card-title"),
                                html.P(
                                    "Visualize survey data across different states.",
                                    className="card-text",
                                ),
                                dbc.Button("View Map", color="primary", href="/statemap"),
                            ]
                        )
                    ),
                    width=4
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Detailed Summaries", className="card-title"),
                                html.P(
                                    "Explore detailed summaries of the survey data.",
                                    className="card-text",
                                ),
                                dbc.Button("View Summary", color="primary", href="/summary"),
                            ]
                        )
                    ),
                    width=4
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Demographics", className="card-title"),
                                html.P(
                                    "Analyze data by various demographic factors.",
                                    className="card-text",
                                ),
                                dbc.Button("View Demographics", color="primary", href="/demographics"),
                            ]
                        )
                    ),
                    width=4
                ),
            ],
            className="mt-4"
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='homepage-graph',
                    figure=px.histogram(df, x='state_code', title='Number of Respondents by State')
                ),
                width=12
            ),
            className="mt-4"
        ),
    ],
    fluid=True,
    className="mt-5"
)
