import numpy as np
import pandas as pd
import plotly.express as px
from mappings import title_dictionary
import random


def weighted_mean(df, value_col, weight_col):
    df = df[df[value_col] != -1]  # Filter out invalid values
    if df.empty or df[weight_col].sum() == 0:
        return np.nan
    return (df[value_col] * df[weight_col]).sum() / df[weight_col].sum()

def weighted_median_interpolated(df, value_col, weight_col='wt'):
    df = df[df[value_col] != -1]  # Filter out invalid values

    if df.empty or df[weight_col].sum() == 0:
        return np.nan  # Handle edge cases

    df = df.sort_values(value_col)  # Sort by category

    cumulative_weight = df[weight_col].cumsum()  # Calculate cumulative weights
    total_weight = df[weight_col].sum()
    cutoff = total_weight / 2.0  # Median cutoff

    idx = cumulative_weight.searchsorted(cutoff)

    if idx == 0:
        return df[value_col].iloc[0] + 0.5  # Start of the first category, assume middle of the range

    lower_value = df[value_col].iloc[idx - 1]
    upper_value = df[value_col].iloc[idx]
    lower_weight = cumulative_weight.iloc[idx - 1]
    upper_weight = cumulative_weight.iloc[idx]

    if cumulative_weight.iloc[idx] == cutoff:
        # If exactly on the cutoff, the median is the midpoint of this category
        return (lower_value + upper_value) / 2.0
    else:
        # Interpolating within the category
        fraction = (cutoff - lower_weight) / (upper_weight - lower_weight)
        return lower_value + fraction

def weighted_frequency(df, value_col, weight_col='wt'):
    """
    Calculate weighted frequencies for given value columns using a specified weight column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    value_col (list): The columns to group by (e.g., [demographic, y_variable]).
    weight_col (str): The name of the column containing the weights.

    Returns:
    pd.DataFrame: A DataFrame with weighted frequencies.
    """

    try:
        # Perform groupby and calculate the sum of weights
        grouped_df = df.groupby(value_col)[weight_col].sum().reset_index()
    except Exception as e:
        print(f"Error during groupby operation: {e}")
        return None  # Return None to indicate failure

    return grouped_df


def aggregate_weighted_frequency(df, groupby_cols, value_col, weight_col='wt'):
    result = df.groupby(groupby_cols).apply(lambda x: weighted_frequency(x, value_col, weight_col).reset_index())
    result = result.reset_index().drop(columns='level_2')
    result.columns = groupby_cols + [value_col, 'Weighted Frequency']
    return result

def aggregate_custom(df, groupby_cols, value_col, result_col_name, agg_func, weight_col='wt', scale_factor=1):
    result = df.groupby(groupby_cols).apply(lambda x: agg_func(x, value_col, weight_col)).reset_index()
    result.columns = groupby_cols + [result_col_name]
    if scale_factor != 1:
        result[result_col_name] = result[result_col_name] / scale_factor
    return result

def get_mapping_dict(selected_variable):
    if selected_variable == 'state':
        return {
            1: 'Alabama', 2: 'Alaska', 4: 'Arizona', 5: 'Arkansas', 6: 'California', 8: 'Colorado',
            9: 'Connecticut', 10: 'Delaware', 11: 'District of Columbia', 12: 'Florida', 13: 'Georgia',
            15: 'Hawaii', 16: 'Idaho', 17: 'Illinois', 18: 'Indiana', 19: 'Iowa', 20: 'Kansas',
            21: 'Kentucky', 22: 'Louisiana', 23: 'Maine', 24: 'Maryland', 25: 'Massachusetts',
            26: 'Michigan', 27: 'Minnesota', 28: 'Mississippi', 29: 'Missouri', 30: 'Montana',
            31: 'Nebraska', 32: 'Nevada', 33: 'New Hampshire', 34: 'New Jersey', 35: 'New Mexico',
            36: 'New York', 37: 'North Carolina', 38: 'North Dakota', 39: 'Ohio', 40: 'Oklahoma',
            41: 'Oregon', 42: 'Pennsylvania', 44: 'Rhode Island', 45: 'South Carolina', 46: 'South Dakota',
            47: 'Tennessee', 48: 'Texas', 49: 'Utah', 50: 'Vermont', 51: 'Virginia', 53: 'Washington',
            54: 'West Virginia', 55: 'Wisconsin', 56: 'Wyoming', 66: 'Guam', 72: 'Puerto Rico', 78: 'Virgin Islands'
        }

    elif selected_variable == 'employment':
        return {
            1: 'Employed',
            2: 'Unemployed',
            3: 'Economically Inactive',
            -1: 'Other'
        }

    elif selected_variable == 'marital_status':
        return {
            1: 'Currently Married',
            2: 'Previously Married',
            3: 'Never Married',
            -1: 'Other'
        }

    elif selected_variable == 'cardiac_event':
        return {
            1: 'Had a heart attack / angina / CHD before',
            2: 'Never had before',
            -1: 'Other'
        }

    elif selected_variable == 'stroke':
        return {
            1: 'Had a stroke before',
            2: 'Never had a stroke before',
            -1: 'Other'
        }

    elif selected_variable == 'mental_health':
        return {
            1: 'Zero days when mental health was not good',
            2: '1-13 days when mental health was not good',
            3: '14+ days when mental health was not good',
            -1: 'Other'
        }

    elif selected_variable == 'medcost':
        return {
            1: 'Couldn’t afford to see doctor in last 12 months',
            2: 'Could afford to see doctor in last 12 months',
            -1: 'Other'
        }

    elif selected_variable == 'checkup':
        return {
            1: 'Within past year',
            2: 'Between 1 and 2 years ago',
            3: 'Between 2 and 5 years ago',
            4: '5 or more years ago',
            8: 'Never',
            -1: 'Other'
        }

    elif selected_variable == 'eye_exam':
        return {
            1: 'Within past month',
            2: 'Past year',
            3: 'Between 1 and 2 years ago',
            4: '2 or more years ago',
            8: 'Never',
            -1: 'Other'
        }

    elif selected_variable == 'physical_health':
        return {
            1: 'Zero days when physical health was not good',
            2: '1-13 days when physical health was not good',
            3: '14+ days when physical health was not good',
            -1: 'Other'
        }

    elif selected_variable == 'poor_health':
        return {
            1: 'Zero days',
            2: '1-13 days',
            3: '14+ days',
            -1: 'Other'
        }

    elif selected_variable == 'stop_smoking':
        return {
            1: 'Attempted to quit smoking in past 12 months',
            2: 'Have not attempted',
            -1: 'Never Smoked / Other'
        }

    elif selected_variable == 'bmi_category':
        return {
            1: 'Underweight',
            2: 'Normal weight',
            3: 'Overweight',
            4: 'Obese',
            -1: 'Other'
        }

    elif selected_variable == 'education':
        return {
            1: 'Did not graduate high school',
            2: 'Graduated high school',
            3: 'Attended college or technical school',
            4: 'Graduated from college or technical school',
            -1: 'Other'
        }

    elif selected_variable == 'general_health':
        return {
            1: 'Good or better health',
            2: 'Fair or poor health',
            -1: 'Other'
        }

    elif selected_variable == 'health_insurance':
        return {
            1: 'Have some form of health insurance',
            2: 'Do not have any form of health insurance',
            -1: 'Other'
        }

    elif selected_variable == 'exercise':
        return {
            1: 'Had physical activity or exercise',
            2: 'No physical activity or exercise in last 30 days',
            -1: 'Other'
        }

    elif selected_variable == 'asthma':
        return {
            1: 'Current',
            2: 'Former',
            3: 'Never',
            -1: 'Other'
        }

    elif selected_variable == 'arthritis':
        return {
            1: 'Diagnosed',
            2: 'Not diagnosed',
            -1: 'Other'
        }

    elif selected_variable == 'sex':
        return {
            1: 'Male',
            2: 'Female',
            -1: 'Other'
        }

    elif selected_variable == 'age':
        return {
            1: 'Age 18-24',
            2: 'Age 25-34',
            3: 'Age 45-54',
            4: 'Age 55-64',
            6: 'Age 65 or older',
            -1: 'Other'
        }

    elif selected_variable == 'height':
        return {}  # continuous variable

    elif selected_variable == 'weight':
        return {}  # continuous variable

    elif selected_variable == 'overweight':
        return {
            1: 'Not overweight or obese',
            2: 'Overweight or obese',
            -1: 'Other'
        }

    elif selected_variable == 'children':
        return {
            1: 'No children in household',
            2: 'One child in household',
            3: '2 children',
            4: '3 children',
            5: '4 children',
            6: '5 or more children',
            -1: 'Other'
        }

    elif selected_variable == 'income': # this mapping is currently only correct for 2021 and 2022
        return {
            1: 'Less than $15,000',
            2: '$15,000 - $25,000',
            3: '$25,000 - $35,000',
            4: '$35,000 - $50,000',
            5: '$50,000 - $100,000',
            6: '$100,000 - $200,000',
            7: '$200,000 or more',
            -1: 'Other'
        }

    elif selected_variable == 'race':
        return {
            1: 'White',
            2: 'Black or African American',
            3: 'American Indian or Alaskan Native',
            4: 'Asian',
            5: 'Native Hawaiian or Other Pacific Islander',
            6: 'Multiracial',
            -1: 'Other'
        }

    elif selected_variable == 'smoking':
        return {
            1: 'Current smoker - now every day',
            2: 'Current smoker - now some days',
            3: 'Former smoker',
            4: 'Never smoked',
            -1: 'Other'
        }

    elif selected_variable == 'binge_drinking':
        return {
            1: 'Did not binge drink in past 30 days',
            2: 'Did binge drink in past 30 days',
            -1: 'Other'
        }

    elif selected_variable == 'heavy_drinking':
        return {
            1: 'Not a heavy drinker',
            2: 'A heavy drinker',
            -1: 'Other'
        }

    elif selected_variable == 'flu_jab':
        return {
            1: 'Over 65 who have had a flu jab in the past year',
            2: 'Over 65 who have not had a flu jab in past year',
            -1: 'Under 65 / Other'
        }

    elif selected_variable == 'pneumonia_jab':
        return {
            1: 'Over 65 who have had a pneumonia jab in past year',
            2: 'Over 65 who have not had a pneumonia jab in past year',
            -1: 'Under 65 / Other'
        }

    elif selected_variable == 'aids_test':
        return {
            1: 'Have been tested for HIV',
            2: 'Have not been tested for HIV',
            -1: 'Other'
        }

    else:
        return {-1: 'Other'}

def update_state_map(selected_year, selected_variable, df, aggregated_data):

    income_data = aggregated_data['income'][aggregated_data['income']['year'] == selected_year].drop(columns=['year'])
    height_data = aggregated_data['height'][aggregated_data['height']['year'] == selected_year].drop(columns=['year'])
    weight_data = aggregated_data['weight'][aggregated_data['weight']['year'] == selected_year].drop(columns=['year'])
    age_data = aggregated_data['age'][aggregated_data['age']['year'] == selected_year].drop(columns=['year'])

    # Merge precomputed data
    merged_data = income_data.merge(height_data, on='state_code', how='inner') \
                             .merge(weight_data, on='state_code', how='inner') \
                             .merge(age_data, on='state_code', how='inner')

    fixed_ranges = {
    'Average Income': (30000, 80000),  # Example range in dollars
    'Average Height': (160, 175),  # Example range in cm
    'Average Weight': (74, 88),  # Example range in kg
    'Average Age': (42, 52)  # Example range in years
    }

    # Create the choropleth map
    choropleth_map = px.choropleth(
        data_frame=merged_data,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color=selected_variable,
        hover_data={
            'Average Income': ':.2f',
            'Average Height': ':.2f',
            'Average Weight': ':.2f',
            'Average Age': ':.2f'
        },
        color_continuous_scale=px.colors.sequential.Blues,
        range_color=fixed_ranges[selected_variable],
        labels={
            'Average Income': 'Average Income ($)',
            'Average Height': 'Average Height (cm)',
            'Average Weight': 'Average Weight (kg)',
            'Average Age': 'Average Age (years)'
        },
    )

    return choropleth_map

def update_frequency_chart(selected_year, selected_variable, df):
    df_filtered = df[df['year'] == selected_year]
    df_grouped = df_filtered.groupby(selected_variable)
    weighted_frequency = df_grouped['wt'].sum().reset_index()
    weighted_frequency.columns = [selected_variable, 'weighted_frequency']
    mapping_dict = get_mapping_dict(selected_variable)
    weighted_frequency['mapped_labels'] = weighted_frequency[selected_variable].map(mapping_dict)

    max_value = weighted_frequency['weighted_frequency'].max()
    max_label = weighted_frequency.loc[weighted_frequency['weighted_frequency'] == max_value, 'mapped_labels'].values[0]

    frequency_chart = px.bar(
        weighted_frequency,
        x='mapped_labels',
        y='weighted_frequency',
        color='weighted_frequency',
        color_continuous_scale=px.colors.sequential.PuBuGn,
        title=f'<b>Adult population count by {selected_variable} in {selected_year}</b>',
        labels={
            'mapped_labels': selected_variable,
            'weighted_frequency': 'Count'
        },
        template='plotly',
        hover_data={'weighted_frequency': ':.2f'},
        text='weighted_frequency'
    )

    # Code to enhance chart layout
    frequency_chart.update_layout(
        title_font_size=24,  # Increase title font size
        xaxis_title=f'<b>{selected_variable}</b>',  # Bold x-axis label
        yaxis_title='<b>Count</b>',  # Bold y-axis label
        margin=dict(t=50, b=50, l=50, r=50),  # Adjust margins
        coloraxis_colorbar=dict(
            title='Count',
            title_font_size=16,
            tickvals=[0, max(weighted_frequency['weighted_frequency'])//2, max(weighted_frequency['weighted_frequency'])],
            ticktext=['Low', 'Medium', 'High']  # Add colorbar tick text
        )
    )

    # Add annotations for key points
    frequency_chart.add_annotation(
        x=max_label,  # x value of max
        y=max_value,  # y value of max
        text="Highest Count",  # Annotation text
        showarrow=True,
        arrowhead=2,
        ax=-50,
        ay=-50
    )

    # Update hover mode
    frequency_chart.update_traces(
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
        textposition='outside',
        texttemplate='%{text:.2s}',
    )

    return f"Selected variable: {selected_variable}", frequency_chart

def filter_and_prepare_data(df, year=None, demographic=None, y_variable=None):
    """
    Filters the DataFrame by the selected demographic variable, then calculates
    the weighted frequency for the y_variable, preparing the data for plotting a time series.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing survey data.
    year (int or None): The selected year to filter the data. If None, data from all years will be used.
    demographic (str): The demographic column to group by (e.g., 'age', 'sex', 'race').
    y_variable (str): The y-axis variable to calculate the weighted frequency for (e.g., 'smoking', 'exercise').

    Returns:
    pd.DataFrame: A DataFrame ready for plotting, with columns for the demographic, y_variable,
                  the weighted frequency, and the percentage of total responses across years.
    """

    # Filter the DataFrame by the selected year if specified, otherwise include all years
    if year:
        df_filtered = df[df['year'] == year]
    else:
        df_filtered = df.copy()

    # Calculate weighted frequency for the y_variable grouped by the demographic and year
    freq_df = df_filtered.groupby(['year', demographic, y_variable])['wt'].sum().reset_index()

    # Calculate total weighted frequency for each demographic category within each year
    total_freq = freq_df.groupby(['year', demographic])['wt'].sum().reset_index()
    total_freq.rename(columns={'wt': 'total_wt'}, inplace=True)

    # Merge to calculate percentage of total for each y_variable category within each demographic group
    merged_df = pd.merge(freq_df, total_freq, on=['year', demographic])
    merged_df['percentage'] = (merged_df['wt'] / merged_df['total_wt']) * 100

    # Prepare the DataFrame for plotting
    plot_df = merged_df[[demographic, y_variable, 'year', 'wt', 'percentage']].copy()
    plot_df.rename(columns={'wt': 'frequency'}, inplace=True)

    plot_df['percentage'] = plot_df['percentage'].round(1)  # Round percentage to 1 decimal place
    plot_df['percentage_text'] = plot_df['percentage'].apply(lambda x: f'{x:.1f}%')
    plot_df['formatted_frequency'] = (plot_df['frequency'] / 1e6).round(2).astype(str) + 'M'  # Convert to millions and format to 2 decimals

    return plot_df


def update_dem_anthro_fig(df, selected_year, demographic, anthro_var):
    """
    Generates the figure for the Anthropometrics & Clinical Measures graph.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing survey data.
    selected_year (int): The year selected by the user.
    demographic (str): The demographic variable selected by the user (e.g., 'age', 'sex').
    anthro_var (str): The specific anthropometric variable to plot (e.g., 'bmi_category').

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure for the Anthropometrics & Clinical Measures.
    """

    # Prepare data
    plot_df = filter_and_prepare_data(df, selected_year, demographic, anthro_var)
    
    # Get the mapping dictionaries for demographic and anthro_var
    demographic_mapping = get_mapping_dict(demographic)
    anthro_mapping = get_mapping_dict(anthro_var)
    
    # Apply the mappings
    plot_df[demographic] = plot_df[demographic].map(demographic_mapping)
    plot_df[anthro_var] = plot_df[anthro_var].map(anthro_mapping)
    
    # Generate Plotly bar chart
    fig = px.bar(
        plot_df,
        x=demographic,
        y='percentage',
        color=anthro_var,
        text='formatted_frequency',
        barmode='group',
        title=f'{title_dictionary[anthro_var]} by {title_dictionary[demographic]} ({selected_year})',
        color_discrete_sequence=randomize_colors(px.colors.qualitative.Set3),
            labels={
            "formatted_frequency": "Frequency",
            "percentage": "Percentage",
            demographic: title_dictionary[demographic],
            anthro_var: title_dictionary[anthro_var]
        },
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',  # Set plot area background to white
        paper_bgcolor='rgba(0,0,0,0)',  # Keep the outer background transparent (or dark)
        font=dict(color='white'),  # Ensure text is visible on the white background
        xaxis=dict(showgrid=False),  # Optional: light gridlines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis_title='Percentage of Demographic Group',
        xaxis_title=title_dictionary[demographic],
        uniformtext_minsize=8, uniformtext_mode='hide'
    )
    
    return fig


def update_dem_chronic_fig(df, selected_year, demographic, chronic_var):
    """
    Generates the figure for the Chronic Conditions graph.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing survey data.
    selected_year (int): The year selected by the user.
    demographic (str): The demographic variable selected by the user (e.g., 'age', 'sex').
    chronic_var (str): The specific chronic condition variable to plot (e.g., 'asthma').

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure for the Chronic Conditions.
    """
    # Prepare data
    plot_df = filter_and_prepare_data(df, selected_year, demographic, chronic_var)
    
    # Get the mapping dictionaries for demographic and chronic_var
    demographic_mapping = get_mapping_dict(demographic)
    chronic_mapping = get_mapping_dict(chronic_var)
    
    # Apply the mappings
    plot_df[demographic] = plot_df[demographic].map(demographic_mapping)
    plot_df[chronic_var] = plot_df[chronic_var].map(chronic_mapping)
    
    # Generate Plotly bar chart
    fig = px.bar(
        plot_df,
        x=demographic,
        y='percentage',
        color=chronic_var,
        text='formatted_frequency',
        barmode='group',
        title=f'{title_dictionary[chronic_var]} by {title_dictionary[demographic]} ({selected_year})',
        color_discrete_sequence=randomize_colors(px.colors.qualitative.Set3),
            labels={
            "formatted_frequency": "Frequency",
            "percentage": "Percentage",
            demographic: title_dictionary[demographic],
            chronic_var: title_dictionary[chronic_var]
        },
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',  # Set plot area background to white
        paper_bgcolor='rgba(0,0,0,0)',  # Keep the outer background transparent (or dark)
        font=dict(color='white'),  # Ensure text is visible on the white background
        xaxis=dict(showgrid=False),  # Optional: light gridlines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis_title='Percentage of Demographic Group',
        xaxis_title=title_dictionary[demographic],
        uniformtext_minsize=8, uniformtext_mode='hide'
    )
    
    return fig


def update_dem_access_fig(df, selected_year, demographic, access_var):
    """
    Generates the figure for the Healthcare Access graph.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing survey data.
    selected_year (int): The year selected by the user.
    demographic (str): The demographic variable selected by the user (e.g., 'age', 'sex').
    access_var (str): The specific healthcare access variable to plot (e.g., 'health_insurance').

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure for Healthcare Access.
    """
    # Prepare data
    plot_df = filter_and_prepare_data(df, selected_year, demographic, access_var)
    
    # Get the mapping dictionaries for demographic and access_var
    demographic_mapping = get_mapping_dict(demographic)
    access_mapping = get_mapping_dict(access_var)
    
    # Apply the mappings
    plot_df[demographic] = plot_df[demographic].map(demographic_mapping)
    plot_df[access_var] = plot_df[access_var].map(access_mapping)
    
    # Generate Plotly bar chart
    fig = px.bar(
        plot_df,
        x=demographic,
        y='percentage',
        color=access_var,
        text='formatted_frequency',
        barmode='group',
        title=f'{title_dictionary[access_var]} by {title_dictionary[demographic]} ({selected_year})',
        color_discrete_sequence=randomize_colors(px.colors.qualitative.Set3),
            labels={
            "formatted_frequency": "Frequency",
            "percentage": "Percentage",
            demographic: title_dictionary[demographic],
            access_var: title_dictionary[access_var]
        },
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',  # Set plot area background to white
        paper_bgcolor='rgba(0,0,0,0)',  # Keep the outer background transparent (or dark)
        font=dict(color='white'),  # Ensure text is visible on the white background
        xaxis=dict(showgrid=False),  # Optional: light gridlines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis_title='Percentage of Demographic Group',
        xaxis_title=title_dictionary[demographic],
        uniformtext_minsize=8, uniformtext_mode='hide'
    )
    
    return fig


def update_dem_health_fig(df, selected_year, demographic, health_var):
    """
    Generates the figure for the Health Measures graph.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing survey data.
    selected_year (int): The year selected by the user.
    demographic (str): The demographic variable selected by the user (e.g., 'age', 'sex').
    health_var (str): The specific health measure variable to plot (e.g., 'blood_pressure').

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure for Health Measures.
    """
    # Prepare data
    plot_df = filter_and_prepare_data(df, selected_year, demographic, health_var)
    
    # Get the mapping dictionaries for demographic and health_var
    demographic_mapping = get_mapping_dict(demographic)
    health_mapping = get_mapping_dict(health_var)
    
    # Apply the mappings
    plot_df[demographic] = plot_df[demographic].map(demographic_mapping)
    plot_df[health_var] = plot_df[health_var].map(health_mapping)
    
    # Generate Plotly bar chart
    fig = px.bar(
        plot_df,
        x=demographic,
        y='percentage',
        color=health_var,
        text='formatted_frequency',
        barmode='group',
        title=f'{title_dictionary[health_var]} by {title_dictionary[demographic]} ({selected_year})',
        color_discrete_sequence=randomize_colors(px.colors.qualitative.Set3),
            labels={
            "formatted_frequency": "Frequency",
            "percentage": "Percentage",
            demographic: title_dictionary[demographic],
            health_var: title_dictionary[health_var]
        },
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',  # Set plot area background to white
        paper_bgcolor='rgba(0,0,0,0)',  # Keep the outer background transparent (or dark)
        font=dict(color='white'),  # Ensure text is visible on the white background
        xaxis=dict(showgrid=False),  # Optional: light gridlines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis_title='Percentage of Demographic Group',
        xaxis_title=title_dictionary[demographic],
        uniformtext_minsize=8, uniformtext_mode='hide'
    )
    
    return fig


def update_dem_lifestyle_fig(df, selected_year, demographic, lifestyle_var):
    """
    Generates the figure for the Lifestyle graph.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing survey data.
    selected_year (int): The year selected by the user.
    demographic (str): The demographic variable selected by the user (e.g., 'age', 'sex').
    lifestyle_var (str): The specific lifestyle variable to plot (e.g., 'smoking').

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure for Lifestyle.
    """
    # Prepare data
    plot_df = filter_and_prepare_data(df, selected_year, demographic, lifestyle_var)
    
    # Get the mapping dictionaries for demographic and lifestyle_var
    demographic_mapping = get_mapping_dict(demographic)
    lifestyle_mapping = get_mapping_dict(lifestyle_var)
    
    # Apply the mappings
    plot_df[demographic] = plot_df[demographic].map(demographic_mapping)
    plot_df[lifestyle_var] = plot_df[lifestyle_var].map(lifestyle_mapping)
    
    # Generate Plotly bar chart
    fig = px.bar(
        plot_df,
        x=demographic,
        y='percentage',
        color=lifestyle_var,
        text='formatted_frequency',
        barmode='group',
        title=f'{title_dictionary[lifestyle_var]} by {title_dictionary[demographic]} ({selected_year})',
        color_discrete_sequence=randomize_colors(px.colors.qualitative.Set3),
            labels={
            "formatted_frequency": "Frequency",
            "percentage": "Percentage",
            demographic: title_dictionary[demographic],
            lifestyle_var: title_dictionary[lifestyle_var]
        },
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',  # Set plot area background to white
        paper_bgcolor='rgba(0,0,0,0)',  # Keep the outer background transparent (or dark)
        font=dict(color='white'),  # Ensure text is visible on the white background
        xaxis=dict(showgrid=False),  # Optional: light gridlines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis_title='Percentage of Demographic Group',
        xaxis_title=title_dictionary[demographic],
        uniformtext_minsize=8, uniformtext_mode='hide'
    )
    
    return fig

def randomize_colors(color_sequence):
    """
    Randomizes the order of a given color sequence.
    
    Parameters:
        color_sequence (list): A list of color hex codes or names.
    
    Returns:
        list: A randomized list of the color sequence.
    """
    randomized_sequence = color_sequence.copy()  # Copy the original sequence
    random.shuffle(randomized_sequence)  # Randomize the order
    return randomized_sequence

def update_life_health_fig(df, selected_year, lifestyle, health_var):
        # Prepare data
    plot_df = filter_and_prepare_data(df, selected_year, lifestyle, health_var)
    
    # Get the mapping dictionaries for lifestyle and health_var
    lifestyle_mapping = get_mapping_dict(lifestyle)
    health_mapping = get_mapping_dict(health_var)
    
    # Apply the mappings
    plot_df[lifestyle] = plot_df[lifestyle].map(lifestyle_mapping)
    plot_df[health_var] = plot_df[health_var].map(health_mapping)
    
    # Generate Plotly bar chart
    fig = px.bar(
        plot_df,
        x=lifestyle,
        y='frequency',
        color=health_var,
        text='percentage_text',
        barmode='stack',
        title=f'{title_dictionary[health_var]} by {title_dictionary[lifestyle]} ({selected_year})',
        color_discrete_sequence=randomize_colors(px.colors.qualitative.Set3),
            labels={
            "formatted_frequency": "Frequency",
            "percentage": "Percentage",
            lifestyle: title_dictionary[lifestyle],
            health_var: title_dictionary[health_var]
        },
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',  # Set plot area background to white
        paper_bgcolor='rgba(0,0,0,0)',  # Keep the outer background transparent (or dark)
        font=dict(color='white'),  # Ensure text is visible on the white background
        xaxis=dict(showgrid=False),  # Optional: light gridlines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis_title='Total Count',
        xaxis_title=title_dictionary[lifestyle],
        uniformtext_minsize=8, uniformtext_mode='hide'
    )
    
    return fig

def update_life_anthro_fig(df, selected_year, lifestyle, anthro_var):
        # Prepare data
    plot_df = filter_and_prepare_data(df, selected_year, lifestyle, anthro_var)
    
    # Get the mapping dictionaries for lifestyle and anthro_var
    lifestyle_mapping = get_mapping_dict(lifestyle)
    anthro_mapping = get_mapping_dict(anthro_var)
    
    # Apply the mappings
    plot_df[lifestyle] = plot_df[lifestyle].map(lifestyle_mapping)
    plot_df[anthro_var] = plot_df[anthro_var].map(anthro_mapping)
    
    # Generate Plotly bar chart
    fig = px.bar(
        plot_df,
        x=lifestyle,
        y='percentage',
        color=anthro_var,
        text='formatted_frequency',
        barmode='stack',
        title=f'{title_dictionary[anthro_var]} by {title_dictionary[lifestyle]} ({selected_year})',
        color_discrete_sequence=randomize_colors(px.colors.qualitative.Set3),
            labels={
            "formatted_frequency": "Frequency",
            "percentage": "Percentage",
            lifestyle: title_dictionary[lifestyle],
            anthro_var: title_dictionary[anthro_var]
        },
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',  # Set plot area background to white
        paper_bgcolor='rgba(0,0,0,0)',  # Keep the outer background transparent (or dark)
        font=dict(color='white'),  # Ensure text is visible on the white background
        xaxis=dict(showgrid=False),  # Optional: light gridlines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        yaxis_title='Percentage of Lifestyle Group',
        xaxis_title=title_dictionary[lifestyle],
        uniformtext_minsize=8, uniformtext_mode='hide'
    )
    
    return fig

def update_life_chronic_fig(df, selected_year, lifestyle, chronic_var, weight_col='wt'):
    """
    Create a heatmap showing the proportional density of each pairing of lifestyle and chronic variable.
    
    Parameters:
    df (pd.DataFrame): The original DataFrame with sample data.
    selected_year (int): The year to filter the data by.
    lifestyle (str): The column name for the lifestyle variable.
    chronic_var (str): The column name for the chronic variable.
    weight_col (str): The column name for the sampling weight (default is 'wt').
    
    Returns:
    fig: Plotly figure object (proportional heatmap).
    """
    
    # Filter the original DataFrame by the selected year
    filtered_df = df[df['year'] == selected_year]
    
    # Get the mapping dictionaries for lifestyle and chronic_var
    lifestyle_mapping = get_mapping_dict(lifestyle)
    chronic_mapping = get_mapping_dict(chronic_var)
    
    # Apply the mappings
    filtered_df[lifestyle] = filtered_df[lifestyle].map(lifestyle_mapping)
    filtered_df[chronic_var] = filtered_df[chronic_var].map(chronic_mapping)
    
    # Calculate weighted frequencies using the provided function
    weighted_df = weighted_frequency(filtered_df, [lifestyle, chronic_var], weight_col=weight_col)
    
    # Normalize the frequencies within each lifestyle group
    weighted_df['normalized_wt'] = weighted_df.groupby(lifestyle)[weight_col].apply(lambda x: x / x.sum())
    
    # Pivot the DataFrame to create a matrix suitable for a heatmap
    heatmap_data = weighted_df.pivot(index=chronic_var, columns=lifestyle, values='normalized_wt').fillna(0)
    
    # Generate a heatmap showing proportions within each lifestyle group
    fig = px.imshow(
        heatmap_data,
        labels=dict(x=title_dictionary[lifestyle], y=title_dictionary[chronic_var], color="Proportion"),
        title=f'Proportional Density of {title_dictionary[chronic_var]} by {title_dictionary[lifestyle]} ({selected_year})',
        color_continuous_scale='Turbo'
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',  # Set plot area background to white
        paper_bgcolor='rgba(0,0,0,0)',  # Keep the outer background transparent (or dark)
        font=dict(color='white'),  # Ensure text is visible on the white background
        xaxis=dict(showgrid=False),  # Optional: light gridlines
        yaxis=dict(showgrid=False),  # Optional: light gridlines
        xaxis_title=title_dictionary[lifestyle],
        yaxis_title=title_dictionary[chronic_var]
    )
    
    return fig


def update_life_access_fig(df, selected_year, lifestyle, access_var, weight_col='wt'):
    """
    Create a violin plot showing the distribution of access variables within lifestyle groups using weighted frequencies.
    
    Parameters:
    df (pd.DataFrame): The original DataFrame with sample data.
    selected_year (int): The year to filter the data by.
    lifestyle (str): The column name for the lifestyle variable.
    access_var (str): The column name for the access variable.
    weight_col (str): The column name for the sampling weight (default is 'wt').
    
    Returns:
    fig: Plotly figure object (violin plot).
    """
    
    # Filter the DataFrame by the selected year
    filtered_df = df[df['year'] == selected_year]
    
    # Aggregate the data by lifestyle and access variable, weighted by the sampling weight
    weighted_df = filtered_df.groupby([lifestyle, access_var])[weight_col].sum().reset_index()
    
    # Normalize weights within each lifestyle group to get proportions
    weighted_df['proportion'] = weighted_df.groupby(lifestyle)[weight_col].apply(lambda x: x / x.sum())

    lifestyle_mapping = get_mapping_dict(lifestyle)
    access_mapping = get_mapping_dict(access_var)
    weighted_df[lifestyle] = weighted_df[lifestyle].map(lifestyle_mapping)
    weighted_df[access_var] = weighted_df[access_var].map(access_mapping)

    # Generate a violin plot
    fig = px.violin(
        weighted_df,
        x=lifestyle,
        y='proportion',
        color=lifestyle,
        box=True,  # Draw a box plot inside the violin
        points='all',  # Show all points
        title=f'Distribution of {title_dictionary[access_var]} by {title_dictionary[lifestyle]} ({selected_year})',
        labels={
            lifestyle: title_dictionary[lifestyle],
            'proportion': f'Proportion of {title_dictionary[access_var]}',
        },
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        xaxis_title=title_dictionary[lifestyle],
        yaxis_title=f'Proportion of {title_dictionary[access_var]}'
    )
    
    return fig


def update_time_series(df, selected_variable):
    """
    Generates a time series plot based on the selected variable.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the survey data.
    selected_variable (str): The variable selected by the user (e.g., 'sex', 'age', 'exercise').

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure representing the time series.
    """

    # Correctly pass the selected variable to y_variable
    time_series_data = filter_and_prepare_data(df, year=None, demographic='age', y_variable=selected_variable)

    # Ensure there is data to plot
    if time_series_data.empty:
        return {}

    # Generate the time series plot
    fig = px.line(
        time_series_data,
        x='year',
        y='frequency',
        color=selected_variable,  # Color by the selected variable
        markers=True,
        title=f'Time Series of {selected_variable.title()} by Age Group (2012-2022)',
        labels={
            selected_variable: selected_variable.title(),
            'percentage': 'Percentage',
            'year': 'Year'
        },
    )
    fig.update_layout(hovermode='x unified')

    return fig

