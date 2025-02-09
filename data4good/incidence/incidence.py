import pandas as pd
from mysoc_dataset import get_dataset_df
import requests
import numpy as np

def get_location():
    response = requests.get('http://ipinfo.io')
    data = response.json()

    loc = data.get('loc', '0,0').split(',')
    latitude = float(loc[0])
    longitude = float(loc[1])
    return latitude, longitude

#Cenlat is my random way of writing latitude (returned from the get_location func) for those who are confused
def find_incidence(cenlat, cenlon):
    df_constituencies = get_dataset_df(
        repo_name="2025-constituencies",
        package_name="parliament_con_2025",
        version_name="latest",
        file_name="parl_constituencies_2025.csv",
        done_survey=True
    )

    latitude_constituency = df_constituencies["center_lat"]
    longitude_constituency = df_constituencies["center_lon"]

    df_crashes = pd.read_excel('data4good/incidence/crash_data2023.xlsx')

    dfnew = [(latitude_constituency.iloc[i] - cenlat) for i in range(len(df_constituencies))]

    dfnew2 = [(longitude_constituency.iloc[i] - cenlon) for i in range(len(df_constituencies))]

    dfnew3 = [np.sqrt(dfnew[i] ** 2 + dfnew2[i] ** 2) for i in range(len(df_constituencies))]

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
    
    percentage_diff = round(((0.3357 - percentage_crash) / percentage_crash) * 100, 3) if percentage_crash else 0

    return percentage_diff

cenlat, cenlon = get_location()
print(find_incidence(cenlat, cenlon))

