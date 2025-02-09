import pandas as pd

# Load the LSOA to constituency mapping
lsoa_to_constituency = pd.read_csv('data/LSOA_(2021)_to_future_Parliamentary_Constituencies_Lookup_in_England_and_Wales.csv', dtype=str)

# Load the accident data
accidents = pd.read_csv('data/new_traffic_accidents.csv', dtype=str)

# Merge the datasets on the LSOA code
merged_data = pd.merge(accidents, lsoa_to_constituency, left_on='lsoa_of_accident_location', right_on='LSOA21CD')

# Filter necessary columns
merged_data = merged_data[['accident_severity', 'PCON25NM']]

# Calculate the total number of accidents for each severity level globally
global_severity = merged_data['accident_severity'].value_counts(normalize=True)

# Calculate the total number of accidents for each severity level within each constituency
constituency_severity = merged_data.groupby(['PCON25NM', 'accident_severity']).size().unstack(fill_value=0).reset_index()

# Rename the columns to match the expected names
constituency_severity.columns = ['PCON25NM', 'Fatal', 'Serious', 'Slight']

# Ensure the severity columns are numeric
constituency_severity[['Slight', 'Serious', 'Fatal']] = constituency_severity[['Slight', 'Serious', 'Fatal']].apply(pd.to_numeric, errors='coerce').fillna(0)

# Calculate the total number of accidents for each constituency
constituency_severity['Total'] = constituency_severity[['Slight', 'Serious', 'Fatal']].sum(axis=1)

# Calculate the proportion of each severity level for each constituency
constituency_severity['Slight_Proportion'] = constituency_severity['Slight'] / constituency_severity['Total']
constituency_severity['Serious_Proportion'] = constituency_severity['Serious'] / constituency_severity['Total']
constituency_severity['Fatal_Proportion'] = constituency_severity['Fatal'] / constituency_severity['Total']

# Normalize the proportions against global averages
constituency_severity['Slight_Proportion'] = constituency_severity['Slight_Proportion'] / global_severity.get('3', 1)
constituency_severity['Serious_Proportion'] = constituency_severity['Serious_Proportion'] / global_severity.get('2', 1)
constituency_severity['Fatal_Proportion'] = constituency_severity['Fatal_Proportion'] / global_severity.get('1', 1)

# Select and rename the required columns
constituency_severity = constituency_severity.rename(columns={
    'Slight_Proportion': 'Normalized_Slight_Proportion',
    'Serious_Proportion': 'Normalized_Serious_Proportion',
    'Fatal_Proportion': 'Normalized_Fatal_Proportion'
})

# Select and rename the required columns
constituency_severity = constituency_severity[['PCON25NM', 'Fatal', 'Serious', 'Slight', 'Total', 'Normalized_Slight_Proportion', 'Normalized_Serious_Proportion', 'Normalized_Fatal_Proportion']]
constituency_severity = constituency_severity.rename(columns={
    'Normalized_Slight_Proportion': 'Slight_Proportion',
    'Normalized_Serious_Proportion': 'Serious_Proportion',
    'Normalized_Fatal_Proportion': 'Fatal_Proportion'
})

# Save the combined data to a CSV file
constituency_severity.to_csv('data/normalised_proportions_of_accidents_by_constituency.csv', index=False)