from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
DATA_DIR = "Neurolytix/backend/data/raw"
FORECAST_DIR = "Neurolytix/backend/data/forecasts"

@router.get("/kpis")
def get_kpis():
    datasets = os.listdir(DATA_DIR)
    forecasts = os.listdir(FORECAST_DIR)
    return {
        "total_datasets": len(datasets),
        "uploaded_today": sum(1 for f in datasets if "2025-09-01" in f),  # Example date
        "total_forecasts": len(forecasts),
        "top_trend_column": "sales"  # Placeholder, could calculate max variance
    }

@router.get("/recent_dataset_trends")
def recent_dataset_trends():
    datasets = os.listdir(DATA_DIR)
    if not datasets:
        return []
    latest = datasets[-1]
    df = pd.read_csv(os.path.join(DATA_DIR, latest))
    df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
    df.dropna(subset=['ds'], inplace=True)
    return df.to_dict(orient="records")

@router.get("/recent_forecasts")
def recent_forecasts():
    forecasts = os.listdir(FORECAST_DIR)
    if not forecasts:
        return []
    latest = forecasts[-1]
    df = pd.read_csv(os.path.join(FORECAST_DIR, latest))
    return df.to_dict(orient="records")
