from dash import dcc, html, register_page, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from mappings import lifestyle_variable_mappings, health_measure_variable_mappings, anthropometric_variable_mappings, health_condition_variable_mappings, healthcare_access_variable_mappings
from helper_functions import update_life_access_fig, update_life_anthro_fig, update_life_health_fig, update_life_condition_fig
from process_data import df

register_page(__name__, name='Lifestyle', path='/lifestyle')

layout = dbc.Container(
    [
        # Instructions
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Button(
                            "How to Use the Graphs", 
                            id="alert-collapse-button-lifestyle", 
                            className="mb-3", 
                            color="primary"
                        ),
                        dbc.Collapse(
                            id="alert-collapse-section-lifestyle",
                            is_open=False,
                            children=dbc.Alert(
                                [
                                    html.H5("How to Use the Graphs", className="alert-heading"),
                                    html.P(
                                        "At the top of the page, you can select a lifestyle variable and a year. "
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
        
        # Top-level Dropdown for Lifestyle Variable Selection
        dbc.Row(
            dbc.Col(
                [
                    html.Label('Select Lifestyle Variable:', className='dropdown-label'),
                    dcc.Dropdown(
                        id='lifestyle-selector-lifestyle',
                        options=lifestyle_variable_mappings,
                        value='smoking',  # Default value
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
                    id='year-slider-lifestyle',
                    min=2012,
                    max=2022,
                    step=1,
                    value=2022,
                    marks={str(year): str(year) for year in range(2012, 2023)},
                    updatemode='drag',
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
                            id='health-measures-selector-lifestyle',
                            options=health_measure_variable_mappings,
                            value='mental_health',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-health-measures-lifestyle', style={'height': '400px'}),
                        html.Div(id='explanation-health-measures-lifestyle', className='text-muted mt-2')
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.Div('Clinical Measures', className='form-label'),
                        dcc.Dropdown(
                            id='anthropometrics-selector-lifestyle',
                            options=anthropometric_variable_mappings,
                            value='bmi_category',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-anthropometrics-lifestyle', style={'height': '400px'}),
                        html.Div(id='explanation-anthropometrics-lifestyle', className='text-muted mt-2')
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
                            id='health-conditions-selector-lifestyle',
                            options=health_condition_variable_mappings,
                            value='asthma',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-health-conditions-lifestyle', style={'height': '400px'}),
                        html.Div(id='explanation-health-conditions-lifestyle', className='text-muted mt-2')
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.Div('Healthcare Access', className='form-label'),
                        dcc.Dropdown(
                            id='healthcare-access-selector-lifestyle',
                            options=healthcare_access_variable_mappings,
                            value='health_insurance',  # Default value
                            clearable=False,
                            className='mb-2'
                        ),
                        dcc.Graph(id='graph-healthcare-access-lifestyle', style={'height': '400px'}),
                        html.Div(id='explanation-healthcare-access-lifestyle', className='text-muted mt-2')
                    ],
                    width=6,
                    className='mx-auto mb-4'
                ),
            ],
            className='mb-4'
        ),
    ],
    fluid=True
)

from dash import callback, Output, Input, State

@callback(
    [
        Output('graph-health-measures-lifestyle', 'figure'),
        Output('graph-anthropometrics-lifestyle', 'figure'),
        Output('graph-health-conditions-lifestyle', 'figure'),
        Output('graph-healthcare-access-lifestyle', 'figure'),
        Output('alert-collapse-section-lifestyle', 'is_open'),  # Add this Output for the alert
    ],
    [
        Input('lifestyle-selector-lifestyle', 'value'),
        Input('year-slider-lifestyle', 'value'),
        Input('health-measures-selector-lifestyle', 'value'),
        Input('anthropometrics-selector-lifestyle', 'value'),
        Input('health-conditions-selector-lifestyle', 'value'),
        Input('healthcare-access-selector-lifestyle', 'value'),
        Input('alert-collapse-button-lifestyle', 'n_clicks'),  # Add this Input for the alert button
    ],
    [State('alert-collapse-section-lifestyle', 'is_open')]  # State to track if the alert is open
)
def update_graphs_and_toggle_alert(lifestyle, selected_year, health_var, anthro_var, condition_var, access_var, n_clicks, is_open):
    # Generate each figure using the respective update function
    fig_health = update_life_health_fig(df, selected_year, lifestyle, health_var)
    fig_anthro = update_life_anthro_fig(df, selected_year, lifestyle, anthro_var)
    fig_condition = update_life_condition_fig(df, selected_year, lifestyle, condition_var)
    fig_access = update_life_access_fig(df, selected_year, lifestyle, access_var)

    # Handle the alert collapse functionality
    if n_clicks:
        is_open = not is_open

    # Return all figures plus the state of the alert collapse
    return fig_health, fig_anthro, fig_condition, fig_access, is_open


