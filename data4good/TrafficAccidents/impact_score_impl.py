import pandas as pd
from mysoc_dataset import get_dataset_df
import filterData as filt

def get_weather_category(weather_description):
    categories = {
        'CLEAR': ["clear sky"],
        'RAIN': ["light rain", "moderate rain", "heavy intensity rain", "very heavy rain", 
                 "extreme rain", "freezing rain"],
        'SNOW': ["light snow", "snow", "heavy snow"],
        'CLOUDY/OVERCAST': ["few clouds", "scattered clouds", "broken clouds", "overcast clouds"],
        'UNKNOWN': [ "dust", "sand"],
        'FOG/SMOKE/HAZE': ["mist", "smoke", "haze", "fog", "sand"],
        'BLOWING SNOW': ["sleet"],
        'FREEZING RAIN/DRIZZLE': ["freezing rain"],
        'OTHER': ["volcanic ash", "squalls", "tornado"],
        'SLEET/HAIL': ["sleet"],
        'SEVERE CROSS WIND GATE': ["windy",  "thunderstorm", "light thunderstorm", "heavy thunderstorm", "ragged thunderstorm" ],
        'BLOWING SAND, SOIL, DIRT': ["dust", "sand"]
    }
    
    # Iterate through the dictionary and find the category
    for category, descriptions in categories.items():
        if weather_description.lower() in [desc.lower() for desc in descriptions]:
            return category
    
    return "Category not found"  # Return this if no category matches

weather_description = filt.get_weather()
hour = filt.get_time()
latitude = filt.get_location()[0]
weather_condition = get_weather_category(weather_description)


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