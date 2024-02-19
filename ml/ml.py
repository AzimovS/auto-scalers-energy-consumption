import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import LSTM, GRU, Dense

df = pd.read_csv('data_points_keda.csv')

timestamps = df['Timestamp'].values.reshape(-1, 1)
values = df['Value'].values

X_train, X_test, y_train, y_test = train_test_split(timestamps, values, test_size=0.1, shuffle=False)

model_choice = '2'

if model_choice == '1':  # Linear Regression
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error on Test Set (Linear Regression):", mse)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    print("Mean Absolute Percentage Error on Test Set (Linear Regression):", mape)

elif model_choice == '2':  # LSTM
    X_train_lstm = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test_lstm = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(1, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    model.fit(X_train_lstm, y_train, epochs=100, verbose=0)

    y_pred_lstm = model.predict(X_test_lstm)
    mse_lstm = mean_squared_error(y_test, y_pred_lstm)
    print("Mean Squared Error on Test Set (LSTM):", mse_lstm)
    mape = np.mean(np.abs((y_test - y_pred_lstm) / y_test)) * 100
    print("Mean Absolute Percentage Error on Test Set (LSTM):", mape)

elif model_choice == '3':  # GRU
    X_train_gru = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test_gru = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    model = Sequential()
    model.add(GRU(50, activation='relu', input_shape=(1, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    model.fit(X_train_gru, y_train, epochs=100, verbose=0)

    y_pred_gru = model.predict(X_test_gru)
    mse_gru = mean_squared_error(y_test, y_pred_gru)
    print("Mean Squared Error on Test Set (GRU):", mse_gru)
    mape = np.mean(np.abs((y_test - y_pred_gru) / y_test)) * 100
    print("Mean Absolute Percentage Error on Test Set (GRU):", mape)

else:
    print("Invalid choice. Please choose 1 for Linear Regression, 2 for LSTM, or 3 for GRU.")
