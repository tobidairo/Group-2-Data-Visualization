from dash import dcc, html, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from mappings import lifestyle_variable_mappings, health_measure_variable_mappings, demographic_variable_mappings, anthropometric_variable_mappings, chronic_condition_variable_mappings, healthcare_access_variable_mappings
from helper_functions import update_dem_access_fig, update_dem_anthro_fig, update_dem_health_fig, update_dem_chronic_fig, update_dem_lifestyle_fig
from process_data import df

register_page(__name__, name='Demographics', path='/demographics')

layout = dbc.Container(
    [
        # Instructions
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Button(
                            "How to Use the Graphs", 
                            id="alert-collapse-button-demographics", 
                            className="mb-3", 
                            color="primary"
                        ),
                        dbc.Collapse(
                            id="alert-collapse-section-demographics",
                            is_open=False,
                            children=dbc.Alert(
                                [
                                    html.H5("How to Use the Graphs", className="alert-heading"),
                                    html.P(
                                        "At the top of the page, you can select a demographic variable and a year. "
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
        
        # Top-level Dropdown for Demographic Variable Selection
        dbc.Row(
            dbc.Col(
                [
                    html.Label('Select Demographic Variable:', className='dropdown-label'),
                    dcc.Dropdown(
                        id='demographic-selector-demographics',
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
                    id='year-slider-demographics',
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
                            id='health-measures-selector-demographics',
                            options=health_measure_variable_mappings,  # Replace with your actual options
                            value='mental_health',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-health-measures-demographics', style={'height': '400px'}),
                        html.Div(id='explanation-health-measures-demographics', className='text-muted mt-2')
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.Div('Lifestyle', className='form-label'),
                        dcc.Dropdown(
                            id='lifestyle-selector-demographics',
                            options=lifestyle_variable_mappings,  # Replace with your actual options
                            value='smoking',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-lifestyle-demographics', style={'height': '400px'}),
                        html.Div(id='explanation-lifestyle-demographics', className='text-muted mt-2')
                    ],
                    width=6
                ),
            ],
            className='mb-4'
        ),

        # Row for Next Two Graphs
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div('Health Conditions', className='form-label'),
                        dcc.Dropdown(
                            id='chronic-conditions-selector-demographics',
                            options=chronic_condition_variable_mappings,  # Replace with your actual options
                            value='asthma',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-chronic-conditions-demographics', style={'height': '400px'}),
                        html.Div(id='explanation-chronic-conditions-demographics', className='text-muted mt-2')
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.Div('Healthcare Access', className='form-label'),
                        dcc.Dropdown(
                            id='healthcare-access-selector-demographics',
                            options=healthcare_access_variable_mappings,  # Replace with your actual options
                            value='health_insurance',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-healthcare-access-demographics', style={'height': '400px'}),
                        html.Div(id='explanation-healthcare-access-demographics', className='text-muted mt-2')
                    ],
                    width=6,
                    className='mx-auto mb-4'
                ),
            ],
            className='mb-4'
        ),
        
        # Centred Last Graph
        dbc.Row(
            dbc.Col(
                    [
                        html.Div('Clinical Measures', className='form-label'),
                        dcc.Dropdown(
                            id='anthropometrics-selector-demographics',
                            options=anthropometric_variable_mappings,  # Replace with your actual options
                            value='bmi_category',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-anthropometrics-demographics', style={'height': '400px'}),
                        html.Div(id='explanation-anthropometrics-demographics', className='text-muted mt-2')
                    ],
                    width=6
                ),
        ),

    ],
    fluid=True
)

from dash import callback, Output, Input, State

@callback(
    [
        Output('graph-anthropometrics-demographics', 'figure'),
        Output('graph-chronic-conditions-demographics', 'figure'),
        Output('graph-healthcare-access-demographics', 'figure'),
        Output('graph-health-measures-demographics', 'figure'),
        Output('graph-lifestyle-demographics', 'figure'),
        Output('alert-collapse-section-demographics', 'is_open'),  # Add this Output for the alert
    ],
    [
        Input('demographic-selector-demographics', 'value'),
        Input('year-slider-demographics', 'value'),
        Input('anthropometrics-selector-demographics', 'value'),
        Input('chronic-conditions-selector-demographics', 'value'),
        Input('healthcare-access-selector-demographics', 'value'),
        Input('health-measures-selector-demographics', 'value'),
        Input('lifestyle-selector-demographics', 'value'),
        Input('alert-collapse-button-demographics', 'n_clicks'),  # Add this Input for the alert button
    ],
    [State('alert-collapse-section-demographics', 'is_open')]  # State to track if the alert is open
)
def update_graphs_and_toggle_alert(demographic, selected_year, anthro_var, chronic_var, access_var, health_var, lifestyle_var, n_clicks, is_open):
    # Generate each figure using the respective update function
    fig_anthro = update_dem_anthro_fig(df, selected_year, demographic, anthro_var)
    fig_chronic = update_dem_chronic_fig(df, selected_year, demographic, chronic_var)
    fig_access = update_dem_access_fig(df, selected_year, demographic, access_var)
    fig_health = update_dem_health_fig(df, selected_year, demographic, health_var)
    fig_lifestyle = update_dem_lifestyle_fig(df, selected_year, demographic, lifestyle_var)

    # Handle the alert collapse functionality
    if n_clicks:
        is_open = not is_open

    # Return all figures plus the state of the alert collapse
    return fig_anthro, fig_chronic, fig_access, fig_health, fig_lifestyle, is_open


