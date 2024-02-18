import requests
import json
import csv
import time
import pandas as pd


CONTAINER_NAME = 'sock-shop-g'

def retrieve_data():
    prometheus_url = "http://localhost:9090/api/v1/query_range" # Your URL
    # Define the query to retrieve the data points
    query = {
        "query": "kepler_container_joules_total", # Your name 
        "start": "2024-02-18T00:00:00Z", # Change dates
        "end": "2024-02-20T00:00:00Z",
        "step": "1m"
    }

    response = requests.get(prometheus_url, params=query)
    data = response.json()
    data_points = dict()
    for res in data["data"]["result"]:
        if res['metric']['container_namespace'] == CONTAINER_NAME:
            data_points[res['metric']['pod_name']]  = res['values']
    return data_points

def write_to_csv(data_dict):
    # Collect all unique timestamps
    timestamps = sorted(set(item[0] for sublist in data_dict.values() for item in sublist))

    with open('data_points_kepler.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header
        header = ["Timestamp"] + list(data_dict.keys())
        csv_writer.writerow(header)
        
        for timestamp in timestamps:
            row = [timestamp]
            for dataset in data_dict.values():
                value = next((item[1] for item in dataset if item[0] == timestamp), '')
                row.append(value)
            csv_writer.writerow(row)


while True:
    data_dict = retrieve_data()
    write_to_csv(data_dict)
    print("Data written to CSV.")
    time.sleep(60)
