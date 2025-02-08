import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = "traffic_accidents.csv"

# Load the latest version
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "oktayrdeki/traffic-accidents",
    file_path,
)

write_path = "data/traffic_accidents.csv"
df.to_csv(write_path, index=False)
