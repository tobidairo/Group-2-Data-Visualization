#pip install pandas, plotly, dash
import pandas as pd
import plotly.express as px

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv('cleaned_data_with_2014_weights.csv')

state_mapping = {
    1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO',
    9: 'CT', 10: 'DE', 11: 'DC', 12: 'FL', 13: 'GA',
    15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA', 20: 'KS',
    21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA',
    26: 'MI', 27: 'MN', 28: 'MS', 29: 'MO', 30: 'MT',
    31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM',
    36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK',
    41: 'OR', 42: 'PA', 44: 'RI', 45: 'SC', 46: 'SD',
    47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA',
    54: 'WV', 55: 'WI', 56: 'WY', 66: 'GU', 72: 'PR', 78: 'VI'
}

df['state_code'] = df['state'].map(state_mapping)

years = df['year'].unique().astype(int)
for year in years:
    print(year)

income_bracket_midpoints = {
    1: 7500,    # Midpoint of "<$15,000"
    2: 20000,   # Midpoint of "$15,000 - $25,000"
    3: 30000,   # Midpoint of "$25,000 - $35,000"
    4: 42500,   # Midpoint of "$35,000 - $50,000"
    5: 75000,   # Midpoint of "$50,000 - $100,000"
    6: 150000,  # Midpoint of "$100,000 - $200,000"
    7: 300000   # Midpoint of "$200,000+" - *some uncertainty (open ended)
}

df['income_midpoint'] = df['income'].map(income_bracket_midpoints)

#getting aggregated data of year and state
income_by_year_state = df.groupby(['year', 'state_code'])['income_midpoint'].mean().reset_index()
income_by_year_state.columns = ['year', 'state_code', 'Average Income']

print(income_by_year_state.head())

app.layout = html.Div([
    html.H1("US INCOME BY STATE", style={'text-align': 'center'}),

    dcc.Slider(
        id='year-slider',
        min=years.min(),
        max=years.max(),
        step=1,
        value=years.min(),
        marks={str(year): str(year) for year in years},
    ),

    dcc.Graph(id='income-by-year-state')
])

@app.callback(
    Output('income-by-year-state', 'figure'),
    [Input('year-slider', 'value')]
)

def update_map(selected_year):
    income_by_year_state_copy = income_by_year_state.copy()
    income_by_year_state_copy = income_by_year_state_copy[income_by_year_state_copy['year'] == selected_year]

    print(f"Data for the year {selected_year}")
    print(income_by_year_state_copy)

    fig = px.choropleth(
        data_frame=income_by_year_state_copy,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='Average Income',
        hover_data=['Average Income'],
        color_continuous_scale=px.colors.sequential.Blues,
        labels={'Average Income': 'Average Income ($)'},
    )

    return fig







if __name__ == '__main__':
    app.run_server(debug=True)