# Neurolytix\backend\forecasting\ensemble.py

import pandas as pd
import numpy as np
from prophet import Prophet
from forecasting.lstm_forecast import LSTMForecaster
import logging

logger = logging.getLogger(__name__)

class EnsembleForecaster:
    def __init__(self, lstm_sequence_length=30, lstm_epochs=50, lstm_batch_size=32, weights=None):
        """
        weights: dict specifying contribution of each model e.g. {"lstm": 0.6, "prophet": 0.4}
        """
        self.lstm_params = {
            "sequence_length": lstm_sequence_length,
            "epochs": lstm_epochs,
            "batch_size": lstm_batch_size
        }
        self.weights = weights or {"lstm": 0.5, "prophet": 0.5}
        self.lstm_model = LSTMForecaster(**self.lstm_params)
        self.prophet_model = None

    def fit_prophet(self, df: pd.DataFrame, target_column: str):
        df_prophet = df.rename(columns={target_column: "y", "ds": "ds"})
        self.prophet_model = Prophet(daily_seasonality=True)
        self.prophet_model.fit(df_prophet)

    def fit_lstm(self, series: pd.Series):
        self.lstm_model.fit(series)

    def fit(self, df: pd.DataFrame, target_column: str):
        logger.info("Fitting ensemble forecaster...")
        self.fit_prophet(df, target_column)
        series = df.set_index("ds")[target_column]
        self.fit_lstm(series)
        logger.info("Ensemble models fitted successfully.")

    def predict(self, df: pd.DataFrame, target_column: str, horizon=30):
        logger.info("Generating ensemble forecast...")
        # Prophet predictions
        future_prophet = self.prophet_model.make_future_dataframe(periods=horizon)
        forecast_prophet = self.prophet_model.predict(future_prophet)
        prophet_pred = forecast_prophet.tail(horizon)[["ds", "yhat"]].reset_index(drop=True)

        # LSTM predictions
        series = df.set_index("ds")[target_column]
        lstm_pred = self.lstm_model.predict(series, horizon=horizon)

        # Combine predictions using weights
        combined = prophet_pred.copy()
        combined["yhat"] = (
            self.weights.get("prophet", 0.5) * prophet_pred["yhat"].values +
            self.weights.get("lstm", 0.5) * lstm_pred["yhat"].values
        )
        return combined
