# DataForGood  

Welcome to **DataForGood**! This project analyzes traffic safety in your area using your **IP address, weather conditions, date, and time**. It leverages the **Kaggle Traffic Accidents dataset** to assess the risk of driving in your location.  

## Dependencies  

To run this project, you will need the following Python libraries:  

- **pandas**  
- **numpy**  
- **mysoc_dataset**  
- **Django**  
- **matplotlib**  
- **seaborn**  

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
    python manage.py runserver
