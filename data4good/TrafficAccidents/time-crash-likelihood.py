import pandas as pd

# Load the crash data
crash_data = pd.read_csv('data/new_traffic_accidents.csv', dtype={'time': str}, low_memory=False)

# Load the time of day data
time_of_day_data = pd.read_csv('data/time_of_day_avg.csv')

# Set the index to 'Time of Day'
time_of_day_data.set_index('Time of Day', inplace=True)

# Calculate the total crashes for each time period
crash_data['Time of Day'] = pd.to_datetime(crash_data['time'], format='%H:%M', errors='coerce').dt.hour
total_crashes = crash_data.groupby('Time of Day').size()

# Create a DataFrame for the likelihood of crashes
likelihood_of_crashes = pd.DataFrame(index=time_of_day_data.index)
likelihood_of_crashes['Total Crashes'] = total_crashes.reindex(likelihood_of_crashes.index).fillna(0)

# Calculate the likelihood of a crash for each time period
likelihood_of_crashes['Likelihood'] = likelihood_of_crashes['Total Crashes'] / time_of_day_data['Average Proportion']

# Function to get the likelihood of a crash for a given hour
def get_crash_likelihood(hour):
    if hour < 0 or hour > 23:
        raise ValueError("Hour must be between 0 and 23")
    if hour not in likelihood_of_crashes.index:
        raise ValueError("Invalid time period")
    return likelihood_of_crashes.loc[hour, 'Likelihood']

# Example usage
hour = int(input("Enter the hour (0-23): ").strip())
crash_likelihood = get_crash_likelihood(hour)
print(f"The likelihood of being in a crash at {hour:02d}:00 is {crash_likelihood:.2f}")