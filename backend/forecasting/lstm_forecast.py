# Neurolytix\backend\forecasting\lstm_forecast.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
import logging

logger = logging.getLogger(__name__)

class LSTMForecaster:
    def __init__(self, sequence_length=30, epochs=50, batch_size=32):
        self.sequence_length = sequence_length
        self.epochs = epochs
        self.batch_size = batch_size
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None

    def _create_sequences(self, data):
        X, y = [], []
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i+self.sequence_length])
            y.append(data[i+self.sequence_length])
        return np.array(X), np.array(y)

    def fit(self, series: pd.Series):
        logger.info("Starting LSTM training...")
        data = series.values.reshape(-1, 1)
        data_scaled = self.scaler.fit_transform(data)

        X, y = self._create_sequences(data_scaled)
        X = X.reshape((X.shape[0], X.shape[1], 1))

        self.model = Sequential()
        self.model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], 1)))
        self.model.add(Dense(1))
        self.model.compile(optimizer='adam', loss='mse')

        early_stop = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)
        self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch_size, callbacks=[early_stop], verbose=1)
        logger.info("LSTM training completed.")

    def predict(self, series: pd.Series, horizon=30):
        data = series.values.reshape(-1, 1)
        data_scaled = self.scaler.transform(data)

        predictions = []
        last_seq = data_scaled[-self.sequence_length:].reshape(1, self.sequence_length, 1)

        for _ in range(horizon):
            pred_scaled = self.model.predict(last_seq, verbose=0)
            predictions.append(pred_scaled[0, 0])
            last_seq = np.append(last_seq[:,1:,:], [[pred_scaled]], axis=1)

        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1,1)).flatten()
        future_dates = pd.date_range(start=series.index[-1]+pd.Timedelta(days=1), periods=horizon)
        forecast_df = pd.DataFrame({'ds': future_dates, 'yhat': predictions})
        return forecast_df
