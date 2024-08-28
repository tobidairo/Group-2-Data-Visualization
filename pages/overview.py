from dash import Dash, dcc, html, register_page, callback, Input, Output
import dash_bootstrap_components as dbc

from process_data import df
from helper_functions import get_mapping_dict, update_state_map, update_frequency_chart, update_time_series, update_overview_bar, get_kpi_card_info
from mappings import population_dropdown_mappings, state_fullname_mappings, demographic_variable_mappings

register_page(__name__, name='Overview', path='/overview')

kpi_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3(id='kpi-card-title', className='card-title'),
            html.P(""),
            dbc.Row(
                [
                    # Left Column
                    dbc.Col(
                        [
                            html.H6("Population:", className="card-text"),
                            html.H4(id='population-display', className="card-value"),
                            html.P(""),
                            html.H6("Average Age:", className="card-text"),
                            html.H4(id='avg-age-display', className="card-value"),
                            html.P(""),
                            html.H6("Employment Rate:", className="card-text"),
                            html.H4(id='employment-display', className="card-value"),
                            html.P(""),
                            html.H6("Median Household Income:", className="card-text"),
                            html.H4(id='income-display', className="card-value"),

                        ],
                    ),
                    # Right Column
                    dbc.Col(
                        [
                            html.H6("Change since last year:", className="card-text"),
                            html.H4(id='population-change-display', className="card-value"),
                            html.P(""),
                            html.H6("Change since last year:", className="card-text"),
                            html.H4(id='avg-age-change-display', className="card-value"),
                            html.P(""),
                            html.H6("Change since last year:", className="card-text"),
                            html.H4(id='employment-change-display', className="card-value"),
                            html.P(""),
                            html.H6("Change since last year:", className="card-text"),
                            html.H4(id='income-change-display', className="card-value"),

                        ],
                    ),
                ]
            ),
        ], className="h-100",
    ),
    className="h-100 kpi-card",
)



# Layout for the "Overview" page
layout = dbc.Container(
    [
        dbc.Row(
            [
                # Overview Block
                dbc.Col(
                    dbc.Container(
                        [
                            html.H2("Overview of CDC Survey Data", className="display-6", style={"color": "black"}),
                            html.P(
                                "Explore key insights and high-level summaries of the CDC Survey data from 2012-2022.",
                                className="lead", style={"color": "black"}
                            ),
                            html.Hr(className="my-2"),
                            html.P(
                                "This page provides an at-a-glance summary of key statistics, trends, and insights over time.", style={"color": "black"}
                            ),
                        ],
                        className="p-4 bg-light rounded-3"
                    ),
                    width=10,
                    style={'marginBottom': '5px', 'marginTop': '5px'}
                ),
                
                # Navigator Menu
                dbc.Col(
                    html.Ul(
                        [
                            html.Li(html.A("State Map Visualization", href="#state-map-section")),
                            html.Li(html.A("Population Breakdown By State, Variable", href="#population-section")),
                            html.Li(html.A("Population Breakdown By Year, Variable", href="#year-section")),
                        ],
                        className="nav flex-column",
                    ),
                    width=2,
                    style={'marginTop': '10px'}
                ),
            ]
        ),

        # State Map Section Subheading
        dbc.Row(
            dbc.Col(
                dbc.Container(
                    [
                        html.H4("State Map Visualization", className="display-7", style={"color": "black", "text-align": "center"}),
                        html.P(
                            "Visual representation of selected variables across different states over time.",
                            className="small", style={"color": "black", "text-align": "center"}
                        ),
                    ],
                    className="p-3 bg-light rounded-3"
                ),
                width=12, style={'marginBottom': '15px', 'marginTop': '50px'}
            ), id="state-map-section",
        ),

        # State Map Layout
        dbc.Row(
            [
                dbc.Col(
                [
                    dbc.Label("Select a state:", html_for='state-selector-overview-2'),
                    dcc.Dropdown(
                        id='state-selector-overview-2',
                        options=state_fullname_mappings,
                        value=1,
                        clearable=False,
                        searchable=True,
                        className="mb-4"
                    ),
                    ],
                    width=5,
                ),

                dbc.Col(
                    html.Div('Select variable:', className='dropdown-label'),
                    width=1
                ),
                
                dbc.Col(
                    html.Div(
                        [
                            dbc.RadioItems(
                                id="variable-selector-state-map",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "Population", "value": "frequency"},
                                    {"label": "Number of Respondents", "value": "count"},
                                ],
                                value="frequency",
                            ),
                        ],
                        className="radio-group",
                    ),
                    width='auto'
                ),
            ],
            className='justify-content-left g-3',
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card, width=5, className='h-100'),
                dbc.Col([
                    html.Div('Select year:', className='form-label'),
                    dcc.Slider(
                        id='year-slider-state-map',
                        min=2012,
                        max=2022,
                        step=1,
                        value=2022,
                        marks={str(year): str(year) for year in range(2012, 2023)},
                        vertical=True,
                        included=False,
                        verticalHeight=500,
                        updatemode='drag',
                    )],
                    width=1,
                ),

                dbc.Col(
                    dcc.Graph(
                        id='choropleth-map-state-map',
                        style={'height': '400px'},
                    ),
                    width=6
                ),

            ],
            className='align-items-center justify-content-center g-3', style={'marginBottom': '5px', 'marginTop': '5px'}
        ),

        # Population Section Subheading
        dbc.Row(
            dbc.Col(
                dbc.Container(
                    [
                        html.H4("Population Breakdown By State, Variable", className="display-7", style={"color": "black", "text-align": "center"}),
                        html.P(
                            "Detailed breakdown of the population by state and selected variables.",
                            className="small", style={"color": "black", "text-align": "center"}
                        ),
                    ],
                    className="p-3 bg-light rounded-3", style={'marginBottom': '5px', 'marginTop': '50px'}
                ),
                width=12
            ), id="population-section",
        ),

        dbc.Row([
            dbc.Col(
                [
                    dbc.Label("Select a state:", html_for='state-selector-overview-1'),
                    dcc.Dropdown(
                        id='state-selector-overview-1',
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
            className="mt-4", style={'marginBottom': '5px', 'marginTop': '5px'}
        ),

        # Year Section Subheading
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
                width=12, style={'marginBottom': '15px', 'marginTop': '50px'}
            ), id="year-section",
        ),

        # Variable Selector and Frequency Chart with Year Slider
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
                        vertical=True,
                        verticalHeight=500,
                        included=False,
                        updatemode='drag',
                    ),
                    width='auto',
                    style={'padding': '10px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}
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
        Output('kpi-card-title', 'children'),
        Output('time-series-graph-overview', 'figure'),
        Output('stacked-bar-chart-overview', 'figure'),
        Output('dd-output-container-overview', 'children'),
        Output('frequency-chart-overview', 'figure'),
        Output('choropleth-map-state-map', 'figure'),
        Output('population-display', 'children'),
        Output('avg-age-display', 'children'),
        Output('employment-display', 'children'),
        Output('income-display', 'children'),
        Output('population-change-display', 'children'),
        Output('avg-age-change-display', 'children'),
        Output('employment-change-display', 'children'),
        Output('income-change-display', 'children'),
    ],
    [
        Input('state-selector-overview-1', 'value'),
        Input('demographic-selector-overview', 'value'),
        Input('year-slider-overview', 'value'),
        Input('variable-selector-overview', 'value'),
        Input('year-slider-state-map', 'value'),
        Input('variable-selector-state-map', 'value'),
        Input('state-selector-overview-2', 'value')
    ]
)
def update_overview(selected_state_1, variable, selected_year, selected_variable, map_year, map_variable, selected_state_2):
    time_series_figure = update_time_series(df, selected_state_1, variable)
    stacked_bar_figure = update_overview_bar(df, selected_state_1, variable)
    
    dropdown_text, frequency_chart = update_frequency_chart(selected_year, selected_variable, df)
    
    state_map = update_state_map(df, map_year, map_variable)

    population, population_change, avg_age, avg_age_change, employment, employment_change, income, income_change = get_kpi_card_info(df, selected_state_2, map_year)

    state_name_mapping = get_mapping_dict('state')

    title = f"{state_name_mapping[selected_state_2]}: Key {map_year} Stats"
    
    return title, time_series_figure, stacked_bar_figure, dropdown_text, frequency_chart, state_map, population, avg_age, employment, income, population_change, avg_age_change, employment_change, income_change
