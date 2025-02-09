import pandas as pd
from mysoc_dataset import get_dataset_df

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
    print(dftest.head())
    return found_location

def fetch_data():
    selected_data = []

    while True:
        data_type = input("Enter the data type (weather, road_surface, time, location, latlong): ").strip().lower()

        file_paths = {
            'weather': 'data/normalised_proportions_weather_conditions.csv',
            'road_surface': 'data/normalised_proportions_road_surface_conditions.csv',
            'location': 'data/normalised_proportions_of_accidents_by_constituency.csv',
            'lookup': 'data/LSOA_(2021)_to_future_Parliamentary_Constituencies_Lookup_in_England_and_Wales.csv',
            'accidents': 'data/new_traffic_accidents.csv',
            'time': 'data/normalised_proportions_by_hour.csv'
        }

        if data_type not in file_paths and data_type != 'latlong':
            print("Invalid data type. Please enter 'weather', 'road_surface', 'location', 'latlong', or 'time'.")
            continue

        if data_type == 'weather':
            df_weather = pd.read_csv(file_paths[data_type])
        elif data_type != 'latlong':
            df = pd.read_csv(file_paths[data_type])

        if data_type == 'weather':
            weather_conditions = {
                1: 'Fine + high winds',
                2: 'Fine no high winds',
                3: 'Fog or mist',
                4: 'Raining + high winds',
                5: 'Raining no high winds',
                6: 'Snowing + high winds',
                7: 'Snowing no high winds',
                8: 'Fine',
                9: 'Fog or mist',
                10: 'High winds',
                11: 'Raining',
                12: 'Snowing'
            }

            print("\nAvailable weather conditions:")
            for key, value in weather_conditions.items():
                print(f"{key}. {value}")

            while True:
                user_input = input("\nEnter the number corresponding to the condition (or type 'done' to finish, 'back' to reselect data type): ").strip()

                if user_input.lower() == 'done':
                    break
                elif user_input.lower() == 'back':
                    break

                try:
                    condition_number = int(user_input)
                    if condition_number not in weather_conditions:
                        print("Invalid condition number.")
                        continue

                    selected_condition = weather_conditions[condition_number]
                    condition_data = df_weather[df_weather['weather_condition'] == selected_condition]
                    selected_data.append((selected_condition, condition_data[['Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']]))
                except ValueError:
                    print("Invalid input. Please enter a number, 'done', or 'back'.")

            if user_input.lower() == 'back':
                continue

        elif data_type == 'road_surface':
            road_surface_conditions = df['road_surface_condition'].unique()
            print("\nAvailable road surface conditions:")
            for i, condition in enumerate(road_surface_conditions, 1):
                print(f"{i}. {condition}")

            while True:
                user_input = input("\nEnter the number corresponding to the road surface condition (or type 'done' to finish, 'back' to reselect data type): ").strip()

                if user_input.lower() == 'done':
                    break
                elif user_input.lower() == 'back':
                    break

                try:
                    condition_number = int(user_input)
                    if condition_number < 1 or condition_number > len(road_surface_conditions):
                        print("Invalid road surface condition number.")
                        continue

                    selected_condition = road_surface_conditions[condition_number - 1]
                    print("Selected road surface condition:", selected_condition)  # Debug statement
                    condition_data = df[df['road_surface_condition'] == selected_condition]
                    selected_data.append((selected_condition, condition_data[['Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']]))
                except ValueError:
                    print("Invalid input. Please enter a number, 'done', or 'back'.")

            if user_input.lower() == 'back':
                continue

        elif data_type == 'location':
            constituencies = df['PCON25NM'].unique()
            print("\nAvailable constituencies:")
            for i, constituency in enumerate(constituencies, 1):
                print(f"{i}. {constituency}")

            while True:
                user_input = input("\nEnter the number corresponding to the constituency (or type 'done' to finish, 'back' to reselect data type): ").strip()

                if user_input.lower() == 'done':
                    break
                elif user_input.lower() == 'back':
                    break

                try:
                    constituency_number = int(user_input)
                    if constituency_number < 1 or constituency_number > len(constituencies):
                        print("Invalid constituency number.")
                        continue

                    selected_constituency = constituencies[constituency_number - 1]
                    print("Selected constituency:", selected_constituency)  # Debug statement
                    constituency_data = df[df['PCON25NM'] == selected_constituency]
                    selected_data.append((selected_constituency, constituency_data[['Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']]))
                except ValueError:
                    print("Invalid input. Please enter a number, 'done', or 'back'.")

            if user_input.lower() == 'back':
                continue

        elif data_type == 'latlong':
            latitude = float(input("Enter latitude: ").strip())
            constituency = find_incidence(latitude)
            print(f"\nConstituency: {constituency}")

            # Load accidents data
            df_accidents = pd.read_csv(file_paths['location'])

            # Find data in accidents file
            constituency_data = df_accidents[df_accidents['PCON25NM'] == constituency]
            selected_data.append((constituency, constituency_data[['Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']]))

        elif data_type == 'time':
            df_time = pd.read_csv(file_paths['time'])
            print("\nAvailable hours:")
            for hour in df_time['hour'].unique():
                print(f"{hour}:00")

            while True:
                user_input = input("\nEnter the hour (0-23) (or type 'done' to finish, 'back' to reselect data type): ").strip()

                if user_input.lower() == 'done':
                    break
                elif user_input.lower() == 'back':
                    break

                try:
                    hour = int(user_input)
                    if hour < 0 or hour > 23:
                        print("Invalid hour.")
                        continue

                    condition_data = df_time[df_time['hour'] == hour]
                    selected_data.append((f"{hour}:00", condition_data[['Slight_Proportion', 'Serious_Proportion', 'Fatal_Proportion']]))
                except ValueError:
                    print("Invalid input. Please enter a number, 'done', or 'back'.")

            if user_input.lower() == 'back':
                continue

        if user_input.lower() == 'done':
            break

    if selected_data:
        print("\nCombined data for selected conditions:")
        combined_data = pd.DataFrame()
        for condition, data in selected_data:
            print(f"\nData for {condition}:")
            print(data.to_string(index=False))
            combined_data = pd.concat([combined_data, data], ignore_index=True)

        # Filter out zero values before calculating the product
        combined_proportions = combined_data[combined_data != 0].prod()
        print("\nCombined proportion values:")
        print(combined_proportions.to_string())

if __name__ == "__main__":
    fetch_data()