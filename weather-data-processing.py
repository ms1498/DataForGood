import pandas as pd
import matplotlib.pyplot as plt

# Adjust pandas display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load the new dataset with low_memory=False to avoid DtypeWarning
file_path = 'data/new_traffic_accidents.csv'
df = pd.read_csv(file_path, dtype={'weather_conditions': str, 'accident_severity': str, 'road_surface_conditions': str}, low_memory=False)

# Ensure the date column is in datetime format and remove the time component
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.date

# Map the weather_conditions numbers to their corresponding descriptions
weather_conditions_map = {
    '1': 'Fine no high winds',
    '2': 'Raining no high winds',
    '3': 'Snowing no high winds',
    '4': 'Fine + high winds',
    '5': 'Raining + high winds',
    '6': 'Snowing + high winds',
    '7': 'Fog or mist',
    '8': 'Other',
    '9': 'Unknown',
    '-1': 'Data missing or out of range'
}
df['weather_condition'] = df['weather_conditions'].map(weather_conditions_map)

# Define accident severity map
accident_severity_map = {
    '1': 'Fatal',
    '2': 'Serious',
    '3': 'Slight'
}
df['accident_severity'] = df['accident_severity'].map(accident_severity_map)

# Filter out unknown and missing data types
df = df[~df['weather_condition'].isin(['Other', 'Unknown', 'Data missing or out of range'])]

# Calculate the total number of collisions for each severity level within each weather condition
severity_collisions = df.groupby(['weather_condition', 'accident_severity']).size().unstack(fill_value=0).reset_index()

# Ensure the severity columns are numeric
severity_collisions[['Slight', 'Serious', 'Fatal']] = severity_collisions[['Slight', 'Serious', 'Fatal']].apply(pd.to_numeric, errors='coerce').fillna(0)

# Calculate the proportion of each severity level for each weather condition
severity_collisions['Total'] = severity_collisions[['Slight', 'Serious', 'Fatal']].sum(axis=1)
severity_collisions['Slight_Proportion'] = severity_collisions['Slight'] / severity_collisions['Total']
severity_collisions['Serious_Proportion'] = severity_collisions['Serious'] / severity_collisions['Total']
severity_collisions['Fatal_Proportion'] = severity_collisions['Fatal'] / severity_collisions['Total']

# Normalise the proportions against "Fine no high winds"
control_proportions = severity_collisions[severity_collisions['weather_condition'] == 'Fine no high winds']
control_slight = control_proportions['Slight_Proportion'].values[0]
control_serious = control_proportions['Serious_Proportion'].values[0]
control_fatal = control_proportions['Fatal_Proportion'].values[0]

severity_collisions['Slight_Proportion'] /= control_slight
severity_collisions['Serious_Proportion'] /= control_serious
severity_collisions['Fatal_Proportion'] /= control_fatal

# Print the normalised proportions for weather conditions
print("Normalised Proportions for Weather Conditions:")
print(severity_collisions[['weather_condition', 'Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']])

# Save the normalised proportions for weather conditions to a CSV file
severity_collisions.to_csv('data/normalised_proportions_weather_conditions.csv', index=False)

# Define the order of the x-axis categories
categories_order = [
    'Fine no high winds', 'Raining no high winds', 'Snowing no high winds',
    'Fine + high winds', 'Raining + high winds', 'Snowing + high winds',
    'Fog or mist'
]

# Plot the normalised proportions in separate bar graphs
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

severity_collisions = severity_collisions.set_index('weather_condition').reindex(categories_order)

# Highlight the control category
colours = ['grey' if x == 'Fine no high winds' else 'blue' for x in severity_collisions.index]

severity_collisions['Slight_Proportion'].plot(kind='bar', ax=axes[0], color=colours)
axes[0].set_xlabel('Weather Condition')
axes[0].set_ylabel('Normalised Proportion of Slight Accidents')
axes[0].set_title('Normalised Proportion of Slight Accidents by Weather Condition (Control: Fine no high winds)')
axes[0].tick_params(axis='x', rotation=45)

colours = ['grey' if x == 'Fine no high winds' else 'orange' for x in severity_collisions.index]

severity_collisions['Serious_Proportion'].plot(kind='bar', ax=axes[1], color=colours)
axes[1].set_xlabel('Weather Condition')
axes[1].set_ylabel('Normalised Proportion of Serious Accidents')
axes[1].set_title('Normalised Proportion of Serious Accidents by Weather Condition (Control: Fine no high winds)')
axes[1].tick_params(axis='x', rotation=45)

colours = ['grey' if x == 'Fine no high winds' else 'red' for x in severity_collisions.index]

severity_collisions['Fatal_Proportion'].plot(kind='bar', ax=axes[2], color=colours)
axes[2].set_xlabel('Weather Condition')
axes[2].set_ylabel('Normalised Proportion of Fatal Accidents')
axes[2].set_title('Normalised Proportion of Fatal Accidents by Weather Condition (Control: Fine no high winds)')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# Create a new column for combined weather conditions
df['combined_weather_condition'] = df['weather_condition'].replace({
    'Fine no high winds': 'Fine',
    'Fine + high winds': 'Fine',
    'Raining no high winds': 'Raining',
    'Raining + high winds': 'Raining',
    'Snowing no high winds': 'Snowing',
    'Snowing + high winds': 'Snowing',
    'Fine + high winds': 'High winds',
    'Raining + high winds': 'High winds',
    'Snowing + high winds': 'High winds'
})

# Calculate the total number of collisions for each severity level within each combined weather condition
combined_severity_collisions = df.groupby(['combined_weather_condition', 'accident_severity']).size().unstack(fill_value=0).reset_index()

# Ensure the severity columns are numeric
combined_severity_collisions[['Slight', 'Serious', 'Fatal']] = combined_severity_collisions[['Slight', 'Serious', 'Fatal']].apply(pd.to_numeric, errors='coerce').fillna(0)

# Calculate the proportion of each severity level for each combined weather condition
combined_severity_collisions['Total'] = combined_severity_collisions[['Slight', 'Serious', 'Fatal']].sum(axis=1)
combined_severity_collisions['Slight_Proportion'] = combined_severity_collisions['Slight'] / combined_severity_collisions['Total']
combined_severity_collisions['Serious_Proportion'] = combined_severity_collisions['Serious'] / combined_severity_collisions['Total']
combined_severity_collisions['Fatal_Proportion'] = combined_severity_collisions['Fatal'] / combined_severity_collisions['Total']

# Normalise the proportions against "Fine"
control_proportions = combined_severity_collisions[combined_severity_collisions['combined_weather_condition'] == 'Fine']
control_slight = control_proportions['Slight_Proportion'].values[0]
control_serious = control_proportions['Serious_Proportion'].values[0]
control_fatal = control_proportions['Fatal_Proportion'].values[0]

combined_severity_collisions['Slight_Proportion'] /= control_slight
combined_severity_collisions['Serious_Proportion'] /= control_serious
combined_severity_collisions['Fatal_Proportion'] /= control_fatal

# Print the normalised proportions for combined weather conditions
print("\nNormalised Proportions for Combined Weather Conditions:")
print(combined_severity_collisions[['combined_weather_condition', 'Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']])

# Save the normalised proportions for combined weather conditions to a CSV file
combined_severity_collisions.to_csv('data/normalised_proportions_combined_weather_conditions.csv', index=False)

# Define the order of the x-axis categories
combined_categories_order = [
    'Fine', 'Raining', 'Snowing', 'High winds'
]

# Plot the normalised proportions in separate bar graphs
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

combined_severity_collisions = combined_severity_collisions.set_index('combined_weather_condition').reindex(combined_categories_order)

# Highlight the control category
colours = ['grey' if x == 'Fine' else 'blue' for x in combined_severity_collisions.index]

combined_severity_collisions['Slight_Proportion'].plot(kind='bar', ax=axes[0], color=colours)
axes[0].set_xlabel('Weather Condition')
axes[0].set_ylabel('Normalised Proportion of Slight Accidents')
axes[0].set_title('Normalised Proportion of Slight Accidents by Combined Weather Condition (Control: Fine)')
axes[0].tick_params(axis='x', rotation=45)

colours = ['grey' if x == 'Fine' else 'orange' for x in combined_severity_collisions.index]

combined_severity_collisions['Serious_Proportion'].plot(kind='bar', ax=axes[1], color=colours)
axes[1].set_xlabel('Weather Condition')
axes[1].set_ylabel('Normalised Proportion of Serious Accidents')
axes[1].set_title('Normalised Proportion of Serious Accidents by Combined Weather Condition (Control: Fine)')
axes[1].tick_params(axis='x', rotation=45)

colours = ['grey' if x == 'Fine' else 'red' for x in combined_severity_collisions.index]

combined_severity_collisions['Fatal_Proportion'].plot(kind='bar', ax=axes[2], color=colours)
axes[2].set_xlabel('Weather Condition')
axes[2].set_ylabel('Normalised Proportion of Fatal Accidents')
axes[2].set_title('Normalised Proportion of Fatal Accidents by Combined Weather Condition (Control: Fine)')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# Map the road_surface_conditions numbers to their corresponding descriptions
road_surface_conditions_map = {
    '1': 'Dry',
    '2': 'Wet or damp',
    '3': 'Snow',
    '4': 'Frost or ice',
    '5': 'Flood over 3cm. deep',
    '6': 'Oil or diesel',
    '7': 'Mud',
    '9': 'Unknown',
    '-1': 'Data missing or out of range'
}
df['road_surface_condition'] = df['road_surface_conditions'].map(road_surface_conditions_map)

# Filter out unknown and missing data types
df = df[~df['weather_condition'].isin(['Other', 'Unknown', 'Data missing or out of range'])]
df = df[~df['road_surface_condition'].isin(['Unknown', 'Data missing or out of range'])]

# Calculate the total number of collisions for each severity level within each road surface condition
road_severity_collisions = df.groupby(['road_surface_condition', 'accident_severity']).size().unstack(fill_value=0).reset_index()

# Ensure the severity columns are numeric
road_severity_collisions[['Slight', 'Serious', 'Fatal']] = road_severity_collisions[['Slight', 'Serious', 'Fatal']].apply(pd.to_numeric, errors='coerce').fillna(0)

# Calculate the proportion of each severity level for each road surface condition
road_severity_collisions['Total'] = road_severity_collisions[['Slight', 'Serious', 'Fatal']].sum(axis=1)
road_severity_collisions['Slight_Proportion'] = road_severity_collisions['Slight'] / road_severity_collisions['Total']
road_severity_collisions['Serious_Proportion'] = road_severity_collisions['Serious'] / road_severity_collisions['Total']
road_severity_collisions['Fatal_Proportion'] = road_severity_collisions['Fatal'] / road_severity_collisions['Total']

# Normalise the proportions against "Dry"
control_proportions = road_severity_collisions[road_severity_collisions['road_surface_condition'] == 'Dry']
control_slight = control_proportions['Slight_Proportion'].values[0]
control_serious = control_proportions['Serious_Proportion'].values[0]
control_fatal = control_proportions['Fatal_Proportion'].values[0]

road_severity_collisions['Slight_Proportion'] /= control_slight
road_severity_collisions['Serious_Proportion'] /= control_serious
road_severity_collisions['Fatal_Proportion'] /= control_fatal

# Print the normalised proportions for road surface conditions
print("\nNormalised Proportions for Road Surface Conditions:")
print(road_severity_collisions[['road_surface_condition', 'Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']])

# Save the normalised proportions for road surface conditions to a CSV file
road_severity_collisions.to_csv('data/normalised_proportions_road_surface_conditions.csv', index=False)

# Define the order of the x-axis categories
road_categories_order = [
    'Dry', 'Wet or damp', 'Snow', 'Frost or ice', 'Flood over 3cm. deep', 'Oil or diesel', 'Mud'
]

# Plot the normalised proportions in separate bar graphs
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

road_severity_collisions = road_severity_collisions.set_index('road_surface_condition').reindex(road_categories_order)

# Highlight the control category
colours = ['grey' if x == 'Dry' else 'blue' for x in road_severity_collisions.index]

road_severity_collisions['Slight_Proportion'].plot(kind='bar', ax=axes[0], color=colours)
axes[0].set_xlabel('Road Surface Condition')
axes[0].set_ylabel('Normalised Proportion of Slight Accidents')
axes[0].set_title('Normalised Proportion of Slight Accidents by Road Surface Condition (Control: Dry)')
axes[0].tick_params(axis='x', rotation=45)

colours = ['grey' if x == 'Dry' else 'orange' for x in road_severity_collisions.index]

road_severity_collisions['Serious_Proportion'].plot(kind='bar', ax=axes[1], color=colours)
axes[1].set_xlabel('Road Surface Condition')
axes[1].set_ylabel('Normalised Proportion of Serious Accidents')
axes[1].set_title('Normalised Proportion of Serious Accidents by Road Surface Condition (Control: Dry)')
axes[1].tick_params(axis='x', rotation=45)

colours = ['grey' if x == 'Dry' else 'red' for x in road_severity_collisions.index]

road_severity_collisions['Fatal_Proportion'].plot(kind='bar', ax=axes[2], color=colours)
axes[2].set_xlabel('Road Surface Condition')
axes[2].set_ylabel('Normalised Proportion of Fatal Accidents')
axes[2].set_title('Normalised Proportion of Fatal Accidents by Road Surface Condition (Control: Dry)')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()