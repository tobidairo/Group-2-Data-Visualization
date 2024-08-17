dtypes = {
    'state': 'int8', 'employment': 'int8', 'marital_status': 'int8', 'cardiac_event': 'int8', 'stroke': 'int8',
    'mental_health': 'int8', 'medcost': 'int8', 'checkup': 'int8', 'eye_exam': 'int8', 'physical_health': 'int8', 
    'poor_health': 'int8', 'stop_smoking': 'int8', 'bmi_category': 'int8', 'education': 'int8', 'general_health': 'int8',
    'health_insurance': 'int8', 'exercise': 'int8', 'asthma': 'int8', 'arthritis': 'int8', 'sex': 'int8', 'age': 'int8',
    'height': 'float64', 'weight': 'float64', 'overweight': 'int8', 'children': 'int8', 'income': 'int8', 'race': 'int8',
    'smoking': 'int8', 'binge_drinking': 'int8', 'heavy_drinking': 'int8', 'flu_jab': 'int8', 'pneumonia_jab': 'int8',
    'aids_test': 'int8', 'wt': 'float64'
}

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

income_bracket_midpoints = {
    1: 7500,    # Midpoint of "<$15,000"
    2: 20000,   # Midpoint of "$15,000 - $25,000"
    3: 30000,   # Midpoint of "$25,000 - $35,000"
    4: 42500,   # Midpoint of "$35,000 - $50,000"
    5: 75000,  # Midpoint of "$50,000 - $100,000"
    6: 150000,  # Midpoint of "$100,000 - $200,000"
    7: 300000,  # Estimated midpoint of "$200,000+"
    -1: -1
}

age_range_midpoints = {
    1: 21.5,
    2: 30,
    3: 40,
    4: 50,
    5: 60,
    6: 75,
    -1: -1
}

state_variable_mappings = [
                            {'label': 'Income', 'value': 'Average Income'},
                            {'label': 'Height', 'value': 'Average Height'},
                            {'label': 'Weight', 'value': 'Average Weight'},
                            {'label': 'Age', 'value': 'Average Age'}
                        ]
population_dropdown_mappings = [
                              {'label': 'State', 'value': 'state'},
                              {'label': 'Employment', 'value': 'employment'},
                              {'label': 'Marital Status', 'value': 'marital_status'},
                              {'label': 'Cardiac Event', 'value': 'cardiac_event'},
                              {'label': 'Stroke', 'value': 'stroke'},
                              {'label': 'Mental Health', 'value': 'mental_health'},
                              {'label': 'Medcost', 'value': 'medcost'},
                              {'label': 'Checkup', 'value': 'checkup'},
                              {'label': 'Eye Exam', 'value': 'eye_exam'},
                              {'label': 'Physical Health', 'value': 'physical_health'},
                              {'label': 'Poor Health', 'value': 'poor_health'},
                              {'label': 'Stop Smoking', 'value': 'stop_smoking'},
                              {'label': 'BMI Category', 'value': 'bmi_category'},
                              {'label': 'Education', 'value': 'education'},
                              {'label': 'General Health', 'value': 'general_health'},
                              {'label': 'Health Insurance', 'value': 'health_insurance'},
                              {'label': 'Exercise', 'value': 'exercise'},
                              {'label': 'Asthma', 'value': 'asthma'},
                              {'label': 'Arthritis', 'value': 'arthritis'},
                              {'label': 'Sex', 'value': 'sex'},
                              {'label': 'Age', 'value': 'age'},
                              {'label': 'Height', 'value': 'height'},
                              {'label': 'Weight', 'value': 'weight'},
                              {'label': 'Overweight', 'value': 'overweight'},
                              {'label': 'Children', 'value': 'children'},
                              {'label': 'Income', 'value': 'income'},
                              {'label': 'Race', 'value': 'race'},
                              {'label': 'Smoking', 'value': 'smoking'},
                              {'label': 'Binge Drinking', 'value': 'binge_drinking'},
                              {'label': 'Heavy Drinking', 'value': 'heavy_drinking'},
                              {'label': 'Flu Jab', 'value': 'flu_jab'},
                              {'label': 'Pneumonia Jab', 'value': 'pneumonia_jab'},
                              {'label': 'AIDS Test', 'value': 'aids_test'}
                          ]