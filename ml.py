from river import time_series
import pandas as pd
from time import sleep

FILENAME = 'emissions.csv'
CSV_COLS = ["timestamp", "emissions",
            "emissions_rate", "cpu_power", "cpu_energy"]
PREDICTED_COL = "emissions"
HORIZON = 1


model = time_series.SNARIMAX(
    p=10,
    d=1,
    q=0,
)

dataframe = pd.read_csv(FILENAME, header=0, usecols=CSV_COLS)

for index, row in dataframe.iterrows():
    model.learn_one(row[PREDICTED_COL])


def get_new_entry():
    dataframe = pd.read_csv(FILENAME, header=0, usecols=CSV_COLS)
    last_entry = dataframe.iloc[-1]
    return last_entry["timestamp"], last_entry[PREDICTED_COL]


df_forecasts = pd.DataFrame({
    'timestamp': [],
    'predicted': [],
    'actual': []
})


predicted_val = None
while True:
    timestamp, new_val = None, None
    if predicted_val:
        timestamp, new_val = get_new_entry()
        model.learn_one(new_val)
        new_row = {'timestamp': timestamp,
                   'predicted': predicted_val, 'actual': new_val}
        df_forecasts = pd.concat(
            [df_forecasts, pd.DataFrame([new_row])], ignore_index=True)

    predicted_val = model.forecast(horizon=HORIZON)[0]
    df_forecasts.to_csv('example.csv', index=False)
    sleep(10)
