import pandas as pd

def read_data(dtypes):
    df = pd.read_csv('data.csv', header=0, dtype=dtypes)
    return df

