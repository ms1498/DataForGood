import pandas as pd
from mysoc_dataset import get_dataset_df

weather_condition = 'Snowing'
hour = 13
latitude = 51.340907

def find_incidence(cenlat):
    df_constituencies = get_dataset_df(
        repo_name="2025-constituencies",
        package_name="parliament_con_2025",
        version_name="latest",
        file_name="parl_constituencies_2025.csv",
        done_survey=True
    )
    latitude_constituency = df_constituencies["center_lat"]

    dfnew = [abs(latitude_constituency.iloc[i] - cenlat) for i in range(len(df_constituencies))]

    ind = dfnew.index(min(dfnew))

    dftest = df_constituencies.iloc[ind]
    found_location = dftest["name"]
    return found_location

def fetch_data(weather_condition, hour, latitude):
    file_paths = {
        'weather': 'TrafficAccidents/data/normalised_proportions_weather_conditions.csv',
        'location': 'TrafficAccidents/data/normalised_proportions_of_accidents_by_constituency.csv',
        'time': 'TrafficAccidents/data/normalised_proportions_by_hour.csv'
    }

    # Load weather data
    df_weather = pd.read_csv(file_paths['weather'])

    # Filter weather data
    weather_data = df_weather[df_weather['weather_condition'] == weather_condition]

    # Load time data
    df_time = pd.read_csv(file_paths['time'])
    time_data = df_time[df_time['hour'] == hour]

    # Find location based on latitude
    constituency = find_incidence(latitude)

    # Load location data
    df_location = pd.read_csv(file_paths['location'])
    location_data = df_location[df_location['PCON25NM'] == constituency]

    # Combine data
    combined_data = pd.concat([weather_data, time_data, location_data], ignore_index=True)

    # Filter out zero values before calculating the product
    combined_proportions = combined_data[combined_data != 0].prod()

    # Print individual and combined proportion values
    # print("\nIndividual Proportion Values:")
    # print(combined_data.to_string(index=False))
    # print("\nCombined Proportion Values, the:")
    # print(combined_proportions.to_string())
    return combined_proportions

fetch_data(weather_condition, hour, latitude)