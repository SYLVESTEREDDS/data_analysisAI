# backend/ai_engine.py

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from datetime import timedelta


class AIEngine:
    """
    Core AI Engine for Neurolytix
    Provides forecasting, clustering, and anomaly detection.
    """

    def __init__(self):
        pass

    # -----------------------------
    # Forecasting
    # -----------------------------
    def forecast(self, data: pd.DataFrame, target_column: str, horizon: int = 10):
        """
        Simple regression-based forecasting.
        Later can extend with Prophet, ARIMA, or Deep Learning models.
        """
        if target_column not in data.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset.")

        # Assume time series indexed by row (can be extended to datetime index)
        X = np.arange(len(data)).reshape(-1, 1)
        y = data[target_column].values

        model = LinearRegression()
        model.fit(X, y)

        # Forecast future points
        future_X = np.arange(len(data), len(data) + horizon).reshape(-1, 1)
        forecast_values = model.predict(future_X)

        forecast_df = pd.DataFrame({
            "step": np.arange(1, horizon + 1),
            "forecast": forecast_values
        })

        return forecast_df.to_dict(orient="records")

    # -----------------------------
    # Clustering
    # -----------------------------
    def cluster(self, data: pd.DataFrame, n_clusters: int = 3):
        """
        Perform clustering on numeric features using KMeans.
        """
        numeric_data = data.select_dtypes(include=[np.number])

        if numeric_data.empty:
            raise ValueError("No numeric data available for clustering.")

        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = model.fit_predict(numeric_data)

        result = data.copy()
        result["cluster"] = labels

        return result.to_dict(orient="records")

    # -----------------------------
    # Anomaly Detection
    # -----------------------------
    def detect_anomalies(self, data: pd.DataFrame, contamination: float = 0.05):
        """
        Detect anomalies in numeric data using Isolation Forest.
        """
        numeric_data = data.select_dtypes(include=[np.number])

        if numeric_data.empty:
            raise ValueError("No numeric data available for anomaly detection.")

        model = IsolationForest(contamination=contamination, random_state=42)
        labels = model.fit_predict(numeric_data)

        result = data.copy()
        result["anomaly"] = ["yes" if label == -1 else "no" for label in labels]

        return result.to_dict(orient="records")
