import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html, register_page, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import df

register_page(__name__, name='Homepage', path='/')

# Introduction and Variables Sections
introduction_text = (
    "This dashboard contains visualizations of selected variables from the CDC BRFSS dataset. "
    "The BRFSS is a health-related survey conducted in the US covering health-related risk behaviors, "
    "chronic health conditions, and the use of preventative services. It provides comprehensive US population data "
    "from diverse variables and has vast applications across public health. "
    "We have created an interactive version of this dataset for researchers to be able to select and specify "
    "information relevant to their area of study."
)

variables_intro = (
    "The variables featured in this dataset have been grouped to allow for comparison across related measures. "
    "These are explained below for your understanding:"
)

# Function to create an expandable card
def create_expandable_card(title, content):
    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Button(title, color="link", id=f"{title}-toggle", n_clicks=0),
                dbc.Collapse(
                    html.Div(content, className="mt-2"),
                    id=f"{title}-collapse",
                    is_open=False,
                ),
            ]
        )
    )

# Variable group details
variable_groups = {
    "Health Measures": [
        "Eye exam – determined when respondents last had an eye exam",
        "General health – respondents’ rating of their general health",
        "Flu jab – respondents over 65 were asked whether they had a flu jab in the past year",
        "Mental health – respondents asked how many days in the past month their mental health was not good",
        "Physical health – respondents asked how many days in the past month their physical health was not good",
        "Poor health – respondents asked how many days in the past month their poor mental or physical health stopped them from disrupted their daily activities",
        "Pneumonia jab – respondents over 65 were asked whether they had a pneumonia jab in the past year",
        "Aids test – respondents were asked whether they had ever been tested for aids",
    ],
    "Lifestyle": [
        "Stop smoking – respondents were asked whether they attempted to quit smoking in the past 12 months",
        "Smoking – determined smoking status (current, former or never) and amount",
        "Exercise – determined whether respondents have had any physical activity in the past 30 days",
        "Binge drinking – determined whether respondents had binge drank in the past 30 days",
        "Heavy drinking – respondents asked whether they are a heavy drinker or not",
    ],
    "Demographics": [
        "Age – groups respondents by age",
        "Sex – separates respondents by sex",
        "State – state where respondent resides",
        "Education – determined the highest level of education obtained by respondent",
        "Children – the number of children respondent has in the household",
        "Income – determined income bracket of respondent",
        "Race – respondents were asked their preferred racial group",
        "Employment – determined employment status of respondents",
        "Marital status – determined marital status of respondents",
    ],
    "Health Conditions": [
        "Asthma – determined whether respondent has or ever had asthma",
        "Stroke – determined whether respondent had ever had a stroke",
        "Arthritis – determined whether respondent has been diagnosed with arthritis",
        "Cardiac event – determined whether respondent has ever had a heart attack, angina or been told they have coronary heart disease",
    ],
    "Clinical Measures": [
        "BMI category – grouped respondents by their BMI",
        "Overweight – determined whether or not respondents featured in the overweight or obese BMI categories",
    ],
    "Healthcare Access": [
        "Medcost – determined whether respondent could afford to see a doctor in the past 12 months",
        "Checkup – determined when respondent last visited a doctor for a routine check up",
        "Health insurance – determined whether respondent has some form of health insurance",
    ],
    "Anthropometric Measurements": [
        "Height – height of respondent",
        "Weight – weight of respondent",
    ],
}

# Creating expandable sections for each variable group
expandable_cards = [
    create_expandable_card(group, html.Ul([html.Li(variable) for variable in details]))
    for group, details in variable_groups.items()
]

# Define the homepage layout
layout = dbc.Container(
    [
        dbc.Row(
        [
            # Left Column: Welcome Message
            dbc.Col(
                dbc.Container(
                    [
                        html.H1("Welcome to the CDC BRFSS Annual Survey Dashboard", className="display-4"),
                        html.P(
                            "This dashboard provides insights and visualizations for the U.S. population "
                            "across various demographics and lifestyle categories, from 2012-2022.",
                            className="lead",
                        ),
                        html.Hr(className="my-2"),
                        html.P(
                            "Use the navigation bar to explore detailed summaries and insights."
                        ),
                        dbc.Button("Get Started", color="primary", href="/overview"),
                    ],
                    className="p-5 bg-light rounded-3"
                ),
                width=8,  # Adjust the width as needed
            ),

            # Right Column: Cards
            dbc.Col(
                [
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
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Lifestyle", className="card-title"),
                                html.P(
                                    "Analyze data by various lifestyle factors.",
                                    className="card-text",
                                ),
                                dbc.Button("View Lifestyle", color="primary", href="/lifestyle"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Chronic Conditions", className="card-title"),
                                html.P(
                                    "Visualize data related to various chronic health conditions.",
                                    className="card-text",
                                ),
                                dbc.Button("View Map", color="primary", href="/chronic_conditions"),
                            ]
                        )
                    ),
                ],
                width=4  # Adjust the width as needed
            ),
        ],
        className="mt-4"
    ),

        
        dbc.Row(
            dbc.Col(
                dbc.Container(
                    [
                        html.H3("Introduction"),
                        html.P(introduction_text),
                        html.Hr(),
                        html.H3("Variable Groups"),
                        html.P(variables_intro),
                        *expandable_cards,
                    ],
                    className="p-4 bg-light rounded-3"
                ),
                width=12
            ),
            className="mt-4"
        ),
    ],
    fluid=True,
    className="mt-5"
)

# Callbacks to handle expandable sections
@callback(
    [Output(f"{title}-collapse", "is_open") for title in variable_groups.keys()],
    [Input(f"{title}-toggle", "n_clicks") for title in variable_groups.keys()],
)
def toggle_expandable(*args):
    ctx = dash.callback_context
    return [not current_state if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == f"{title}-toggle" else current_state
            for current_state, title in zip(args, variable_groups.keys())]
