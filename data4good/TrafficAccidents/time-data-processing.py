import pandas as pd

# Load the accident data
file_path = 'data/new_traffic_accidents.csv'
df = pd.read_csv(file_path, dtype={'weather_conditions': str, 'accident_severity': str, 'road_surface_conditions': str}, low_memory=False)

# Ensure the date and time columns are in datetime format
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M')

# Extract the hour from the datetime column
df['hour'] = df['datetime'].dt.hour

# Map the accident_severity numbers to their corresponding descriptions
accident_severity_map = {
    '1': 'Fatal',
    '2': 'Serious',
    '3': 'Slight'
}
df['accident_severity'] = df['accident_severity'].map(accident_severity_map)

# Group by hour and accident severity and count the number of accidents
severity_by_hour = df.groupby(['hour', 'accident_severity']).size().unstack(fill_value=0).reset_index()

# Ensure the severity columns are numeric
severity_by_hour[['Slight', 'Serious', 'Fatal']] = severity_by_hour[['Slight', 'Serious', 'Fatal']].apply(pd.to_numeric, errors='coerce').fillna(0)

# Calculate the total number of accidents for each hour
severity_by_hour['Total'] = severity_by_hour[['Slight', 'Serious', 'Fatal']].sum(axis=1)

# Calculate the proportion of each severity level for each hour
severity_by_hour['Slight_Proportion'] = severity_by_hour['Slight'] / severity_by_hour['Total']
severity_by_hour['Serious_Proportion'] = severity_by_hour['Serious'] / severity_by_hour['Total']
severity_by_hour['Fatal_Proportion'] = severity_by_hour['Fatal'] / severity_by_hour['Total']

# Calculate the global averages for each severity level
global_severity = df['accident_severity'].value_counts(normalize=True)
global_slight = global_severity.get('Slight', 1)
global_serious = global_severity.get('Serious', 1)
global_fatal = global_severity.get('Fatal', 1)

# Normalise the proportions against global averages
severity_by_hour['Slight_Proportion'] /= global_slight
severity_by_hour['Serious_Proportion'] /= global_serious
severity_by_hour['Fatal_Proportion'] /= global_fatal

# Print the normalised proportions for each hour
print("Normalised Proportions for Each Hour:")
print(severity_by_hour[['hour', 'Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']])

# Save the normalised proportions for each hour to a CSV file
severity_by_hour.to_csv('data/normalised_proportions_by_hour.csv', index=False)