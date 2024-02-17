import requests
import json
import csv
import time

def retrieve_data():
    prometheus_url = "http://localhost:9090/api/v1/query_range"
    # Define the query to retrieve the data points
    query = {
        "query": "carbon_aware_keda_scaler_carbon_intensity",
        "start": "2024-02-15T00:00:00Z",
        "end": "2024-02-18T00:00:00Z",
        "step": "1m"
    }

    response = requests.get(prometheus_url, params=query)
    data = response.json()
    data_points = data["data"]["result"][0]["values"]
    data_dict = {}
    for timestamp, value in data_points:
        data_dict[timestamp] = value

    return data_dict

def write_to_csv(data_dict):
    with open('data_points.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'Value'])
        for timestamp, value in data_dict.items():
            writer.writerow([timestamp, value])

while True:
    data_dict = retrieve_data()
    print(data_dict)
    write_to_csv(data_dict)
    print("Data written to CSV.")
    time.sleep(60)
