import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pytz
import TrafficAccidents.filterData as fil
import io
import base64

def myCoolFunc():
    sns.set_theme(style="whitegrid", palette="flare")
    matplotlib.use('Agg')  # Use a non-interactive backend

    filtered_df = fil.filter_data()
    file_path = "TrafficAccidents/traffic_accidents.csv"
    df = pd.read_csv(file_path)

    # Plot 1: Injury Severity by Hour
    plt.figure(figsize=(10, 5))
    injury_columns = [
        'injuries_total', 'injuries_fatal', 'injuries_incapacitating',
        'injuries_non_incapacitating', 'injuries_reported_not_evident'
    ]
    df['hour_bin'] = (df['crash_hour'] // 3) * 3
    injury_by_hour_bin = df.groupby('hour_bin')[injury_columns].sum().sum(axis=1)
    plt.figure(figsize=(10, 6))
    plt.pie(injury_by_hour_bin, labels=[f'{x}:00-{x+3}:00' for x in injury_by_hour_bin.index], autopct='%1.1f%%', startangle=140)
    plt.title("Total Injuries Distribution by 3-Hour Interval")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot1 = base64.b64encode(img.getvalue()).decode()

    # Plot 3: Crash Type Distribution
    injury_counts = filtered_df.groupby(['trafficway_type', 'most_severe_injury']).size().unstack().fillna(0)
    injury_counts.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title("Injury Severity by Road Type (Stacked)")
    plt.xlabel('Trafficway Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()  
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot3 = base64.b64encode(img.getvalue()).decode()

    # Plot 4: Severity of Injuries by Traffic Control Device
    plt.figure(figsize=(10, 5))
    device_counts = filtered_df['traffic_control_device'].value_counts()
    min_threshold = 100  # Change this value if needed
    valid_devices = device_counts[device_counts > min_threshold].index
    filtered_data = filtered_df[filtered_df['traffic_control_device'].isin(valid_devices)]

    # Plot the filtered data
    sns.countplot(data=filtered_data, x='traffic_control_device', hue='most_severe_injury')
    plt.title("Severity of Injuries by Traffic Control Device (Filtered)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot4 = base64.b64encode(img.getvalue()).decode()

    # Plot 5: Intersection-Related Accidents by Injury Type
    plt.figure(figsize=(10, 5))
    temp_df = df[~df['prim_contributory_cause'].isin(['NOT APPLICABLE', 'UNABLE TO DETERMINE'])]
    top_10_causes = temp_df['prim_contributory_cause'].value_counts().index[:10]
    sns.countplot(data=temp_df, y='prim_contributory_cause', order=top_10_causes)
    plt.title("Primary Contributory Causes of Accidents")
    plt.tight_layout()  
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot5 = base64.b64encode(img.getvalue()).decode()
    # plt.show()

    # Plot 8: Primary Contributory Causes of Accidents
    plt.figure(figsize=(10, 5))
    injury_columns = ['injuries_total', 'injuries_fatal', 'injuries_incapacitating', 'injuries_non_incapacitating', 'injuries_reported_not_evident']
    filtered_df.groupby('lighting_condition')[injury_columns].sum().plot(kind='bar', stacked=True, figsize=(10, 5))
    plt.title("Total Injuries by Lighting Condition")
    plt.ylabel("Number of Injuries")
    plt.tight_layout()  
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot6 = base64.b64encode(img.getvalue()).decode()
    # plt.show()

    # Plot 9: Extent of Damage Based on Road Defects
    plt.figure(figsize=(10, 6))
    sns.countplot(data=filtered_df, x='most_severe_injury')

    plt.title(f"Injury Severity for CLEAR", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.xlabel("Most Severe Injury", fontsize=12)
    plt.ylabel("Count of Accidents", fontsize=12)
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot2 = base64.b64encode(img.getvalue()).decode()
    # plt.show()


    context = {
        "plot1" : plot1,
        "plot2" : plot2,
        "plot3" : plot3,
        "plot4" : plot4,
        "plot5" : plot5,
        "plot6" : plot6,
               }

    return context