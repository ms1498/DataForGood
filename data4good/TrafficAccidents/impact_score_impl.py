import pandas as pd
import numpy as np
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
latitude = float(latitude)
longitude = float(longitude)
hour = int(filt.get_time(latitude,longitude))
#api_key = "ad36e519250ce7c8dc131ebe1c0d561d"
#weather_description = filt.get_weather(latitude, longitude, api_key)
weather_description = "windy"
weather_condition = get_weather_category(weather_description)
weather_condition = 'Fine + high winds'


def find_incidence(cenlat, cenlon):
    
    df_constituencies = pd.read_csv("incidence/parl2025.csv")
    latitude_constituency = df_constituencies["center_lat"]
    longitude_constituency = df_constituencies["center_lon"]


    df_crashes = pd.read_excel('incidence/crash_data2023.xlsx')

    dfnew = [(latitude_constituency.iloc[i] - cenlat) for i in range(len(df_constituencies))]

    dfnew2 = [(longitude_constituency.iloc[i] - cenlon) for i in range(len(df_constituencies))]

    dfnew3 = [ np.sqrt(dfnew[i] ** 2 + dfnew2[i] ** 2) for i in range(len(df_constituencies))]

    ind = dfnew3.index(min(dfnew3))

    dftest = df_constituencies.iloc[ind]
    found_location = dftest["gss_code"]
    found_electorate = dftest["electorate"]

    print(found_location)

    crash_amount_place = df_crashes[df_crashes["LSOA"] == found_location]

    if not crash_amount_place.empty:
        crash_amount = max(crash_amount_place["Casualties"])
    else:
        crash_amount = 0

    percentage_crash = (crash_amount / (found_electorate * 0.615)) * 100 if found_electorate else 0

    percentage_diff = round(((percentage_crash - 0.3357) / 0.3357 ) * 5, 3) if percentage_crash else 0

    return percentage_diff

def fetch_data(weather_condition, hour, latitude):
    file_paths = {
        'weather': 'data/normalised_proportions_weather_conditions.csv',
        'location': 'data/normalised_proportions_of_accidents_by_constituency.csv',
        'time': 'data/normalised_proportions_by_hour.csv'
    }

    # Load weather data
    df_weather = pd.read_csv(file_paths['weather'])

    # Filter weather data
    weather_data = df_weather[df_weather['weather_condition'] == weather_condition]

    # Load time data
    df_time = pd.read_csv(file_paths['time'])
    time_data = df_time[df_time['hour'] == hour]

    # Find location based on latitude
    constituency = find_incidence(latitude, longitude)

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