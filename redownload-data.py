import os
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

print("You must have a Kaggle account and a Kaggle API key to download the dataset. The Kaggle.json file must be stored in system root ('~/.kaggle/' for Unix-based systems or 'C:\\Users\\<YourUsername>\\.kaggle\\' for Windows). Please refer to the Kaggle API documentation for more information.")
# Authenticate with Kaggle API
api = KaggleApi()
api.authenticate()

# Download the dataset
dataset = 'oktayrdeki/traffic-accidents'
api.dataset_download_files(dataset, path='data/', unzip=True)

# Load the dataset into a pandas DataFrame
file_path = 'data/traffic_accidents.csv'  # Path to the downloaded dataset
df = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(df.head())