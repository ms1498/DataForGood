import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pytz
import filterData as fil 

def myCoolFunc():
    filtered_df = fil.filter_data()

    # Plot 1: Injury Severity by Hour
    plt.figure(figsize=(10, 5))
    sns.countplot(data=filtered_df, x='most_severe_injury', order=filtered_df['most_severe_injury'].value_counts().index)
    plt.title("Injury Severity Distribution")
    plt.xticks(rotation=45)
    plot1 = plt
    # plt.show()

    # Plot 2: Injury Severity by Road Type
    plt.figure(figsize=(10, 5))
    sns.countplot(data=filtered_df, x='trafficway_type', hue='most_severe_injury')
    plt.title("Injury Severity by Road Type")
    plt.xticks(rotation=45)
    plot2 = plt
    # plt.show()

    # Plot 3: Crash Type Distribution
    plt.figure(figsize=(10, 5))
    sns.countplot(data=filtered_df, x='crash_type', order=filtered_df['crash_type'].value_counts().index)
    plt.title("Crash Type Distribution")
    plt.xticks(rotation=45)
    plot3 = plt
    # plt.show()

    # Plot 4: Severity of Injuries by Traffic Control Device
    plt.figure(figsize=(10, 5))
    sns.countplot(data=filtered_df, x='traffic_control_device', hue='most_severe_injury')
    plt.title("Severity of Injuries by Traffic Control Device")
    plt.xticks(rotation=45)
    plot4 = plt
    # plt.show()

    # Plot 5: Intersection-Related Accidents by Injury Type
    plt.figure(figsize=(10, 5))
    sns.countplot(data=filtered_df, x='intersection_related_i', hue='most_severe_injury')
    plt.title("Intersection-Related Accidents by Injury Type")
    plot5 = plt
    # plt.show()

    # Plot 8: Primary Contributory Causes of Accidents
    plt.figure(figsize=(10, 5))
    sns.countplot(data=filtered_df, y='prim_contributory_cause', order=filtered_df['prim_contributory_cause'].value_counts().index[:10])
    plt.title("Primary Contributory Causes of Accidents")
    plot6 = plt
    # plt.show()

    # Plot 9: Extent of Damage Based on Road Defects
    plt.figure(figsize=(10, 5))
    sns.countplot(data=filtered_df, x='road_defect', hue='damage')
    plt.title("Extent of Damage Based on Road Defects")
    plt.xticks(rotation=45)
    plot7 = plt
    # plt.show()

    # Plot 10: Total Injuries by Lighting Condition
    plt.figure(figsize=(10, 5))
    injury_columns = ['injuries_total', 'injuries_fatal', 'injuries_incapacitating', 'injuries_non_incapacitating', 'injuries_reported_not_evident']
    filtered_df.groupby('lighting_condition')[injury_columns].sum().plot(kind='bar', stacked=True, figsize=(10, 5))
    plt.title("Total Injuries by Lighting Condition")
    plt.ylabel("Number of Injuries")
    plot8 = plt
    # plt.show()

    context = {
        "plot1" : plot1,
        "plot2" : plot2,
        "plot3" : plot3,
        "plot4" : plot4,
        "plot5" : plot5,
        "plot6" : plot6,
        "plot7" : plot7,
        "plot8" : plot8,
               }