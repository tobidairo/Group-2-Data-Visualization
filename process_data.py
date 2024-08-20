import pandas as pd
from mappings import state_mapping, income_bracket_midpoints, age_range_midpoints

def read_data(dtypes):
    df = pd.read_csv('data.csv', header=0, dtype=dtypes)

    df['state_code'] = df['state'].map(state_mapping)

    df['income_midpoint'] = df['income'].map(income_bracket_midpoints)

    df['age_midpoint'] = df['age'].map(age_range_midpoints)

    return df

