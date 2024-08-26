from dash import dcc, html, register_page, callback, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from process_data import df
from mappings import chronic_condition_variable_mappings, health_measure_variable_mappings, anthropometric_variable_mappings, lifestyle_variable_mappings, healthcare_access_variable_mappings
from helper_functions import update_chronic_access_fig, update_chronic_health_fig, update_chronic_lifestyle_fig, update_chronic_anthro_fig

register_page(__name__, name='Chronic Conditions', path='/chronic_conditions')


layout = dbc.Container(
    [
        # Instructions
        dbc.Row(
            dbc.Col(
                [
                    dbc.Button(
                        "How to Use the Graphs", 
                        id="alert-collapse-button-chronic-condition", 
                        className="mb-3", 
                        color="primary"
                    ),
                    dbc.Collapse(
                        id="alert-collapse-section-chronic-condition",
                        is_open=False,
                        children=dbc.Alert(
                            [
                                html.H5("How to Use the Graphs", className="alert-heading"),
                                html.P(
                                    "At the top of the page, you can select a chronic condition variable and a year. "
                                    "These selections will apply to all graphs below. "
                                    "Each graph represents a different category. "
                                    "You can further refine each graph by selecting additional variables specific to that category."
                                ),
                                html.P(
                                    "To interact with the graphs, use the legend:"
                                ),
                                html.Ul(
                                    [
                                        html.Li("Double-click on a legend item to isolate and view only that category."),
                                        html.Li("Single-click on a legend item to exclude that category from the graph."),
                                    ]
                                ),
                                html.P(
                                    "Have fun exploring the data!"
                                ),
                            ],
                            color="info",  # Adjust if needed for the SLATE theme
                            dismissable=False,
                            style={"padding": "20px", "border-radius": "5px"}
                        )
                    )
                ],
                width={"size": 12, "offset": 0}
            ),
            className="mb-4"
        ),

        #Top-level Dropdown for Chronic Condition Variable Selection
        dbc.Row(
            dbc.Col(
                [
                    html.Label('Select Chronic Condition Variable:', className='dropdown-label'),
                    dcc.Dropdown(
                        id='chronic-condition-dropdown',
                        options=chronic_condition_variable_mappings,  # Replace with your actual options
                        value='stroke',  # Default value
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
                    id='year-slider-chronic-condition',
                    updatemode='drag',
                    min=2012,
                    max=2022,
                    step=1,
                    value=2022,
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
                        html.Div('Health Measures', className='form-label'),
                        dcc.Dropdown(
                            id='health-measures-dropdown',
                            options=health_measure_variable_mappings,
                            value='mental_health',
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='health-measures-chronic-condition-graph', style={'height': '400px'}),
                        html.Div(id='explanation-health-measures', className='text-muted mt-2')
                    ],
                    width=6
                ),

                dbc.Col(
                    [
                        html.Div('Clinical Measures', className='form-label'),
                        dcc.Dropdown(
                            id='anthropometric-dropdown',
                            options=anthropometric_variable_mappings,
                            value='bmi_category',
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='anthropometric-chronic-condition-graph', style={'height': '400px'}),
                        html.Div(id='explanation-anthropometrics', className='text-muted mt-2')
                    ],
                    width=6
                ),
            ],
        ),

        # Row for Second Two Graphs
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div('Lifestyle', className='form-label'),
                        dcc.Dropdown(
                            id='lifestyle-dropdown',
                            options=lifestyle_variable_mappings,
                            value='smoking',
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='lifestyle-chronic-condition-graph', style={'height': '400px'}),
                        html.Div(id='explanation-lifestyle', className='text-muted mt-2')
                    ],
                    width=6
                ),

                dbc.Col(
                    [
                        html.Div('Healthcare Access', className='form-label'),
                        dcc.Dropdown(
                            id='healthcare-access-dropdown',
                            options=healthcare_access_variable_mappings,
                            value='health_insurance',
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='healthcare-access-chronic-condition-graph', style={'height': '400px'}),
                        html.Div(id='explanation-healthcare-access', className='text-muted mt-2')
                    ],
                    width=6
                ),
            ],
        ),
    ],
    fluid=True
)

# Callbacks
from dash import callback, Output, Input, State

@callback(
    [
        Output('anthropometric-chronic-condition-graph', 'figure'),
        Output('health-measures-chronic-condition-graph', 'figure'),
        Output('lifestyle-chronic-condition-graph', 'figure'),
        Output('healthcare-access-chronic-condition-graph', 'figure'),
        Output('alert-collapse-section-chronic-condition', 'is_open')
    ],
    [
        Input('chronic-condition-dropdown', 'value'),
        Input('anthropometric-dropdown', 'value'),
        Input('health-measures-dropdown', 'value'),
        Input('lifestyle-dropdown', 'value'),
        Input('healthcare-access-dropdown', 'value'),
        Input('year-slider-chronic-condition', 'value'),
        Input('alert-collapse-button-chronic-condition', 'n_clicks')
    ],
    [State('alert-collapse-section-chronic-condition', 'is_open')]
)

def update_graphs_and_toggle_alert(chronic_condition, anthro_var, health_var, lifestyle_var, access_var, selected_year, n_clicks, is_open):
    # Generate each figure using the respective update function
    fig_chronic_anthro = update_chronic_anthro_fig(df, selected_year, chronic_condition, anthro_var)
    fig_chronic_health = update_chronic_health_fig(df, selected_year, chronic_condition, health_var)
    fig_chronic_lifestyle = update_chronic_lifestyle_fig(df, selected_year, chronic_condition, lifestyle_var)
    fig_chronic_access = update_chronic_access_fig(df, selected_year, chronic_condition, access_var)
    # Handle the alert collapse functionality
    if n_clicks:
        is_open = not is_open

    return fig_chronic_anthro, fig_chronic_health, fig_chronic_lifestyle, fig_chronic_access, is_open