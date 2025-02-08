import pandas as pd
from mysoc_dataset import get_dataset_df
import requests

def get_location():
    response = requests.get('http://ipinfo.io')
    data = response.json()

    loc = data.get('loc', '0,0').split(',')
    latitude = float(loc[0])
    longitude = float(loc[1])
    return latitude, longitude


#Cenlat is my random way of writing latitude (returned from the get_location func) for those who are confused
def find_incidence(cenlat):
    df_constituencies = get_dataset_df(
        repo_name="2025-constituencies",
        package_name="parliament_con_2025",
        version_name="latest",
        file_name="parl_constituencies_2025.csv",
        done_survey=True
    )
    latitude_constituency = df_constituencies["center_lat"]

    df_crashes = pd.read_excel('data4good/incidence/crash_data2023.xlsx')

    dfnew = [abs(latitude_constituency.iloc[i] - cenlat) for i in range(len(df_constituencies))]

    ind = dfnew.index(min(dfnew))

    dftest = df_constituencies.iloc[ind]  
    found_location = dftest["gss_code"]
    found_electorate = dftest["electorate"]

    #This is the nearest found constituency, pls remove if need be
    print(found_location)

    crash_amount_place = df_crashes[df_crashes["LSOA"] == found_location]

    crash_amount = max(crash_amount_place["Casualties"])

    percentage_crash = (crash_amount / (found_electorate*0.615))*100
    
    percentage_diff = round(((0.3357 - percentage_crash)/percentage_crash)*100, 3)

    return percentage_diff

cenlat, cenlon = get_location()
print(find_incidence(cenlat))


