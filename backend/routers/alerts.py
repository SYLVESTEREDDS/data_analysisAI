from fastapi import APIRouter, HTTPException, Query
from alerts.alert_service import AlertService
from analytics.anomaly_detection import AnomalyDetector
import pandas as pd
import os

router = APIRouter()
DATA_DIR = "Neurolytix/backend/data/raw"

# Configure your SMTP credentials
alert_service = AlertService(
    email_user="your_email@gmail.com",
    email_pass="your_email_password"
)

@router.get("/alert_anomalies")
def alert_anomalies(dataset_id: str = Query(...), target_column: str = Query(...), user_email: str = Query(...)):
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

        detector = AnomalyDetector(method="zscore")
        anomalies = detector.detect(df[target_column])

        if not anomalies.empty:
            message = f"⚠️ Anomaly Alert for Dataset {dataset_id}, Column {target_column}\n\n"
            message += anomalies.to_string()
            alert_service.send_email(user_email, f"Neurolytix Anomaly Alert: {dataset_id}", message)
            return {"message": f"Alert sent to {user_email}", "anomalies_detected": len(anomalies)}
        else:
            return {"message": "No anomalies detected"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alerting failed: {str(e)}")
