import os
import json
import time
import requests
import pandas as pd

def retrieve_data(query):
    prometheus_url = "http://localhost:9090/api/v1/"
    params = {'query': query}
    try:
        response = requests.get(prometheus_url + 'query', params=params)
        response.raise_for_status()  # Raise an exception for 4XX/5XX status codes
        data = response.json()
        result_values = data["data"]["result"]
        power_consumption_data = []
        for value in result_values:
            pod_power_consumption = value["metric"]
            pod_power_consumption["value"] = float(value["value"][1])
            power_consumption_data.append(pod_power_consumption)
        return power_consumption_data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def write_to_csv(data_dict):
    if os.path.isfile("data/teastore_power_data.csv"):
        pd.DataFrame(data_dict).to_csv("data/teastore_power_data.csv", mode='a', header=False, index=False)
    else:
        pd.DataFrame(data_dict).to_csv("data/teastore_power_data.csv", index=False)

while True:
    query = "sum by (pod_name, container_name, container_namespace, node) ( irate(kepler_container_joules_total{}[1m]) )"
    data_dict = retrieve_data(query)
    print(data_dict)
    write_to_csv(data_dict)
    print("Data written to CSV.")
    time.sleep(60)