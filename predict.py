import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

def exponential_weighting(data, alpha):
    weighted_data = [data[0]]  # First data point remains the same
    for i in range(1, len(data)):
        weighted_value = alpha * data[i] + (1 - alpha) * weighted_data[i-1]
        weighted_data.append(weighted_value)
    return weighted_data

def predict(stock_data, duration, future):
    stock_data = stock_data[["Date", "Close"]]

    # Preprocess the data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(stock_data["Close"].values.reshape(-1, 1))

    # Apply exponential weighting to the data
    alpha = 0.2  # Adjust the alpha parameter as needed
    weighted_data = exponential_weighting(scaled_data.flatten(), alpha)

    # Prepare the data for LSTM model
    X = weighted_data
    y = scaled_data

    # Split the data into training and testing sets
    train_size = int(len(X) * 0.8)
    train_data, test_data = X[:train_size], X[train_size:]
    train_labels, test_labels = y[:train_size], y[train_size:]

    # Create sequences and labels for training set
    sequence_length = future  # Adjust as needed
    X_train, y_train = [], []
    for i in range(len(train_data) - sequence_length):
        X_train.append(train_data[i:i+sequence_length])
        y_train.append(train_labels[i+sequence_length])
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Build and train the LSTM model
    model = Sequential()
    model.add(LSTM(units=100, return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=100))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=100, batch_size=60)

    # Predict future prices
    future_prices = []
    last_sequence = np.array(X[-sequence_length:]).reshape(1, sequence_length, 1)
    for _ in range(future):
        next_price = model.predict(last_sequence)
        future_prices.append(next_price[0, 0])
        last_sequence = np.append(last_sequence[:, 1:, :], next_price.reshape(1, 1, 1), axis=1)

    # Scale back the predicted prices
    future_prices = scaler.inverse_transform(np.array(future_prices).reshape(-1, 1))
    return future_prices
