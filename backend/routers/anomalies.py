from fastapi import APIRouter, Query, HTTPException
import pandas as pd
import os
from analytics.anomaly_detection import AnomalyDetector

router = APIRouter()
DATA_DIR = "Neurolytix/backend/data/raw"

@router.get("/detect_anomalies")
def detect_anomalies(dataset_id: str = Query(...), target_column: str = Query(...), method: str = Query("zscore")):
    try:
        files = os.listdir(DATA_DIR)
        dataset_file = next((f for f in files if f.startswith(dataset_id)), None)
        if not dataset_file:
            raise HTTPException(status_code=404, detail="Dataset not found.")

        df = pd.read_csv(os.path.join(DATA_DIR, dataset_file))
        if target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column {target_column} not in dataset.")

        df[target_column] = pd.to_numeric(df[target_column], errors='coerce')
        df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
        df.dropna(subset=['ds', target_column], inplace=True)
        df.set_index('ds', inplace=True)

        detector = AnomalyDetector(method=method)
        if method == "isolation_forest":
            detector.fit(df[target_column])
        anomalies = detector.detect(df[target_column])
        return anomalies.reset_index().to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detection failed: {str(e)}")
