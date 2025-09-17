# Neurolytix\backend\services\forecasting_engine.py

import pandas as pd
from prophet import Prophet

class ForecastingEngine:
    """
    Core forecasting engine for Neurolytix.
    Supports basic time series forecasting.
    """

    def __init__(self):
        # You can initialize multiple models here for ensemble
        pass

    def forecast(self, df: pd.DataFrame, target_column: str, horizon: int = 30):
        """
        Forecast the target column for the next 'horizon' periods.
        Returns a dictionary of predicted values and confidence intervals.
        """
        # Ensure the dataset has a 'ds' datetime column
        if 'ds' not in df.columns:
            raise ValueError("Dataset must contain a 'ds' column for datetime values.")

        if df[target_column].isnull().any():
            df[target_column] = df[target_column].fillna(method='ffill')

        # Prepare data for Prophet
        prophet_df = df[['ds', target_column]].rename(columns={target_column: 'y'})

        # Fit Prophet model
        model = Prophet(daily_seasonality=True)
        model.fit(prophet_df)

        # Create future dataframe
        future = model.make_future_dataframe(periods=horizon)
        forecast = model.predict(future)

        # Extract predictions for forecast horizon
        forecast_horizon = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(horizon)
        result = forecast_horizon.to_dict(orient='records')

        return result
