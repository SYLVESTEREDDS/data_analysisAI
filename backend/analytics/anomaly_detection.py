# Neurolytix\backend\analytics\anomaly_detection.py

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self, method="zscore", threshold=3):
        """
        method: "zscore" or "isolation_forest"
        threshold: Z-score threshold
        """
        self.method = method
        self.threshold = threshold
        self.model = None

    def fit(self, series: pd.Series):
        if self.method == "isolation_forest":
            self.model = IsolationForest(contamination=0.05, random_state=42)
            self.model.fit(series.values.reshape(-1, 1))

    def detect(self, series: pd.Series):
        anomalies = pd.DataFrame(index=series.index)
        anomalies["value"] = series.values

        if self.method == "zscore":
            mean = series.mean()
            std = series.std()
            anomalies["zscore"] = (series - mean) / std
            anomalies["anomaly"] = anomalies["zscore"].abs() > self.threshold

        elif self.method == "isolation_forest":
            pred = self.model.predict(series.values.reshape(-1, 1))
            anomalies["anomaly"] = pred == -1

        else:
            raise ValueError("Unsupported method for anomaly detection")

        detected = anomalies[anomalies["anomaly"]]
        logger.info(f"Detected {len(detected)} anomalies using {self.method}")
        return detected
