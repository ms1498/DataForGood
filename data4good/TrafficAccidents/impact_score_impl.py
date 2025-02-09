import pandas as pd
from mysoc_dataset import get_dataset_df
import TrafficAccidents.filterData as filt

def get_weather_category(weather_description):
    categories = {
        'Fine + high winds': ["windy"],
        'Fine no high winds': ["clear sky", "few clouds", "scattered clouds", "broken clouds", "overcast clouds", "haze", "fog"],
        'Raining + high winds': [ "squalls", "tornado"],
        'Raining no high winds': ["light rain", "moderate rain", "heavy rain", "light thunderstorm", "heavy thunderstorm", "ragged thunderstorm"],
        'Snowing + high winds': ["heavy snow", "snow"],
        'Snowing no high winds': ["light snow", "sleet", "freezing rain"],
        'Fine': ["clear sky","few clouds", "scattered clouds", "broken cloud", "overcast clouds"],
        'High winds':[ "windy", "squalls", "tornado"],
        'Raining': ["light rain"," moderate rain"," heavy rain", "light thunderstorm", "heavy thunderstorm", "ragged thunderstorm"],
        'Snowing': ["light snow", "snow", "heavy snow"]

    }
    
    # Iterate through the dictionary and find the category
    for category, descriptions in categories.items():
        if weather_description.lower() in [desc.lower() for desc in descriptions]:
            return category
    
    return "Category not found"  # Return this if no category matches

latitude, longitude = filt.get_location()
print(latitude)
hour = int(filt.get_time(latitude,longitude))
#api_key = "ad36e519250ce7c8dc131ebe1c0d561d"
#weather_description = filt.get_weather(latitude, longitude, api_key)
weather_description = "windy"
weather_condition = get_weather_category(weather_description)
weather_condition = 'Fine + high winds'


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
    print(combined_proportions[6])
    return [combined_proportions[5], combined_proportions[6], combined_proportions[7]]

fetch_data(weather_condition, hour, latitude)