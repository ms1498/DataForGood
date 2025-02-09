import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import requests


# Get current time at the coordinates (latitude, longitude)
def get_time(lat,lon):
    # Get the timezone based on GPS coordinates using TimezoneFinder
    lat = float(lat)
    lon = float(lon)
    
    tz_finder = TimezoneFinder()
    timezone_str = tz_finder.timezone_at(lng=lon, lat=lat)
    
    # Get the current time in that timezone
    local_timezone = pytz.timezone(timezone_str)
    local_time = datetime.now(local_timezone)
    
    return local_time.strftime('%H')
    #return local_time.strftime('%Y-%m-%d %H:%M:%S')

def get_location():
    # Make a request to ipinfo.io API
    response = requests.get('http://ipinfo.io')
    data = response.json()
    
    # Extract latitude and longitude
    loc = data.get('loc', '0,0').split(',')
    latitude = loc[0]
    longitude = loc[1]
    
    return latitude, longitude

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

# Get weather based on GPS coordinates (latitude, longitude)
def get_weather(lat, lon, api_key):
    # OpenWeatherMap API endpoint for current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        # Make the API request
        response = requests.get(url)
        
        # Check if the response status is OK (200)
        if response.status_code == 200:
            data = response.json()
            
            # Check if the necessary data exists in the response
            if "weather" in data and "main" in data:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                
                # Return the weather information
                weather_info = {
                    "weather": weather
                }
                return weather
            else:
                return {"error": "Invalid response structure from OpenWeatherMap."}
        else:
            # Handle non-200 responses from the API
            return {"error": f"Unable to fetch weather data. HTTP Status Code: {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions during the request
        return {"error": f"An error occurred: {e}"}

def filter_data():
    
    latitude, longitude = get_location()
    #api_key = "ad36e519250ce7c8dc131ebe1c0d561d"
    current_time = int(get_time(latitude, longitude))
    #weather_description = get_weather(latitude, longitude, api_key)
    #weather_condition = get_weather_category(weather_description)\
    weather_condition = "CLEAR"

    file_path = "data4good/TrafficAccidents/traffic_accidents.csv"
    file_path = "TrafficAccidents/traffic_accidents.csv"
    df = pd.read_csv(file_path)

    file_path = "TrafficAccidents/traffic_accidents.csv"
    df = pd.read_csv(file_path)
    
    return df[(df['crash_hour'] >= current_time-1) & (df['crash_hour'] <= current_time+1) & (df['weather_condition'] == weather_condition)]
