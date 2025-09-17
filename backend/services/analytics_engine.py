# backend/analytics_engine.py

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.arima.model import ARIMA
import os
import uuid
import json

class AnalyticsEngine:
    def __init__(self, data_dir="backend/data"):
        self.data_dir = data_dir
        os.makedirs(f"{data_dir}/forecasts", exist_ok=True)
        os.makedirs(f"{data_dir}/clusters", exist_ok=True)
        os.makedirs(f"{data_dir}/anomalies", exist_ok=True)

    # 📊 Load dataset by ID
    def load_dataset(self, dataset_id: str) -> pd.DataFrame:
        path = f"{self.data_dir}/raw/{dataset_id}.csv"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset {dataset_id} not found")
        return pd.read_csv(path)

    # 🔮 Forecasting (ARIMA)
    def generate_forecast(self, dataset_id: str, target_column: str, horizon: int = 10):
        df = self.load_dataset(dataset_id)
        if target_column not in df.columns:
            raise ValueError(f"Column {target_column} not found in dataset")

        series = df[target_column].dropna()

        model = ARIMA(series, order=(5, 1, 0))
        model_fit = model.fit()

        forecast = model_fit.forecast(steps=horizon)
        forecast_id = str(uuid.uuid4())

        result = {
            "forecast_id": forecast_id,
            "dataset_id": dataset_id,
            "target_column": target_column,
            "horizon": horizon,
            "forecast_values": forecast.tolist(),
        }

        with open(f"{self.data_dir}/forecasts/{forecast_id}.json", "w") as f:
            json.dump(result, f)

        return result

    # 🔍 Clustering (KMeans)
    def generate_clusters(self, dataset_id: str, n_clusters: int = 3):
        df = self.load_dataset(dataset_id)
        numeric_df = df.select_dtypes(include=[np.number]).dropna()

        if numeric_df.empty:
            raise ValueError("No numeric data available for clustering")

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(numeric_df)

        cluster_id = str(uuid.uuid4())
        result = {
            "cluster_id": cluster_id,
            "dataset_id": dataset_id,
            "n_clusters": n_clusters,
            "labels": clusters.tolist(),
            "centroids": kmeans.cluster_centers_.tolist(),
        }

        with open(f"{self.data_dir}/clusters/{cluster_id}.json", "w") as f:
            json.dump(result, f)

        return result

    # ⚡ Anomaly Detection (Isolation Forest)
    def detect_anomalies(self, dataset_id: str, target_column: str):
        df = self.load_dataset(dataset_id)
        if target_column not in df.columns:
            raise ValueError(f"Column {target_column} not found in dataset")

        series = df[[target_column]].dropna()

        model = IsolationForest(contamination=0.1, random_state=42)
        df["anomaly"] = model.fit_predict(series)

        anomalies = df[df["anomaly"] == -1]

        anomaly_id = str(uuid.uuid4())
        result = {
            "anomaly_id": anomaly_id,
            "dataset_id": dataset_id,
            "target_column": target_column,
            "n_anomalies": len(anomalies),
            "anomalies": anomalies.to_dict(orient="records"),
        }

        with open(f"{self.data_dir}/anomalies/{anomaly_id}.json", "w") as f:
            json.dump(result, f)

        return result
