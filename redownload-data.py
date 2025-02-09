import os
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Set the path to the Kaggle file you'd like to load
kaggle_file_path = "traffic_accidents.csv"

# Load the latest version of the Kaggle dataset
kaggle_df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "oktayrdeki/traffic-accidents",
    kaggle_file_path,
)

# Save the Kaggle dataset to a local file
kaggle_write_path = "data/traffic_accidents.csv"
kaggle_df.to_csv(kaggle_write_path, index=False)

# Set the URL to the new dataset
url = "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2023.csv"

# Load the new dataset
new_df = pd.read_csv(url)

# Save the new dataset to a separate local file
new_write_path = "data/new_traffic_accidents.csv"
new_df.to_csv(new_write_path, index=False)