import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
# from pyngrok import ngrok
from mappings import dtypes, state_mapping, income_bracket_midpoints, age_range_midpoints, state_variable_mappings, population_dropdown_mappings
from helper_functions import weighted_mean, weighted_median_interpolated, weighted_frequency, aggregate_weighted_frequency, aggregate_custom, get_mapping_dict, update_state_map

print('Reading data...')
df = pd.read_csv('data.csv', header=0, dtype=dtypes)
print('Read data.')

df['state_code'] = df['state'].map(state_mapping)

df['income_midpoint'] = df['income'].map(income_bracket_midpoints)

df['age_midpoint'] = df['age'].map(age_range_midpoints)

# Aggregate data for continuous variables
print('Aggregating data...')
aggregated_data = {
    'income': aggregate_custom(
        df, groupby_cols=['year', 'state_code'], value_col='income_midpoint', result_col_name='Average Income', agg_func=weighted_mean
    ),
    'height': aggregate_custom(
        df, groupby_cols=['year', 'state_code'], value_col='height', result_col_name='Average Height', agg_func=weighted_mean
    ),
    'weight': aggregate_custom(
        df, groupby_cols=['year', 'state_code'], value_col='weight', result_col_name='Average Weight', agg_func=weighted_mean, scale_factor=100
    ),
    'age': aggregate_custom(
        df, groupby_cols=['year', 'state_code'], value_col='age_midpoint', result_col_name='Average Age', agg_func=weighted_mean
    )
}
print('Finished aggregating data.')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Header(
        html.H1("Demographics", style={'text-align': 'center', 'padding': '10px'}),
    ),

    # Variable selector and Year slider
    html.Div(
        [
            html.Div(
                [
                    dcc.RadioItems(
                        id='variable-selector',
                        options=state_variable_mappings,
                        value='Average Income',
                        labelStyle={'display': 'inline-block', 'margin-right': '100px',}
                    ),
                ],
                style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}
            ),
            html.Div(
                [
                    dcc.Slider(
                        id='year-slider',
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
                dcc.Graph(id='choropleth-map', style={'height': '500px'}),
                style={'width': '48%', 'display': 'inline-block', 'padding': '20px','flex-grow': '1'}
            ),
            html.Div(
                dcc.Graph(id='column-chart', style={'height': '500px'}),
                style={'width': '48%', 'display': 'inline-block', 'padding': '20px', 'flex-grow': '1'}
            ),
        ],
        style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}
    ),

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

@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('column-chart', 'figure'),
     Output('dd-output-container-2', 'children'),
     Output('frequency-chart', 'figure')],
    [Input('year-slider', 'value'),
     Input('variable-selector', 'value'),
     Input('variable-selector-2', 'value')]
)

def update_plots(selected_year, selected_variable, selected_variable_2):
    return(update_state_map(selected_year, selected_variable, selected_variable_2, df, aggregated_data))

def run_dash_app():
    app.run_server(port=8050, debug=True)

run_dash_app()




