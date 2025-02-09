# Safe2Drive  

Welcome to **Safe2Drive**! This project analyzes traffic safety in your area using your **IP address, weather conditions, date, and time**. It leverages the **Kaggle Traffic Accidents dataset** to assess the risk of driving in your location.  

# Our Impact

Safe2Drive utilises data from a number of sources including the Kaggle Traffic Accidents Dataset to provide users with a risk factor for their driving. This is calculated based on their rough location from their IP address, the weather in their area and the time of day. These come together to form on main risk factor score, informing the driver of how dangerous their driving could be, and providing personalised reccomendations based on their information to help the user improve their safety.

The user can also see their score broken down into their overall likelihood of a crash and the possible severities of a crash if it were to occur. They can also view all other statistics for their locations, weather and date


## Dependencies  

To run this project, you will need the following Python libraries:  

- **pandas**  
- **numpy**  
- **mysoc_dataset**  
- **Django**  
- **matplotlib**  
- **seaborn**
- **timezonefinder**

### API Key Requirement  

This project requires an API key for the **OpenWeatherMap API** to retrieve real-time weather data. You can get a free API key (limited to **1,000 requests per month**) from:  

🔗 [OpenWeatherMap API](https://openweathermap.org/api)  

Use the following endpoint format in your code:  

http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric

Store this in TrafficAccidents.filterData on line 100.

## How to Run  

1. Navigate to the project directory:  
   ```sh
   cd data4good
2. Start the Django development server:
   ```sh
    python manage.py runserver
