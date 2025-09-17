from fastapi import APIRouter, Query, HTTPException
import pandas as pd
import os
from analytics.forecast_evaluation import ForecastEvaluator

router = APIRouter()
FORECAST_DIR = "Neurolytix/backend/data/forecasts"
DATA_DIR = "Neurolytix/backend/data/raw"

@router.get("/compare_forecasts")
def compare_forecasts(dataset_id: str = Query(...), actual_column: str = Query(...)):
    # Load actual dataset
    dataset_file = next((f for f in os.listdir(DATA_DIR) if f.startswith(dataset_id)), None)
    if not dataset_file:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df_actual = pd.read_csv(os.path.join(DATA_DIR, dataset_file))
    if actual_column not in df_actual.columns:
        raise HTTPException(status_code=400, detail=f"Column {actual_column} not found in dataset")

    df_actual[actual_column] = pd.to_numeric(df_actual[actual_column], errors='coerce')
    df_actual['ds'] = pd.to_datetime(df_actual['ds'], errors='coerce')
    df_actual.dropna(subset=['ds', actual_column], inplace=True)
    df_actual.set_index('ds', inplace=True)

    # Load forecast models for the dataset
    model_files = [f for f in os.listdir(FORECAST_DIR) if f.startswith(dataset_id)]
    if not model_files:
        raise HTTPException(status_code=404, detail="No forecasts found for this dataset")

    models_forecasts = {}
    for file in model_files:
        model_name = file.replace(f"{dataset_id}_", "").replace(".csv", "")
        df_forecast = pd.read_csv(os.path.join(FORECAST_DIR, file))
        df_forecast['yhat'] = pd.to_numeric(df_forecast['yhat'], errors='coerce')
        df_forecast['ds'] = pd.to_datetime(df_forecast['ds'], errors='coerce')
        df_forecast.dropna(subset=['ds', 'yhat'], inplace=True)
        df_forecast.set_index('ds', inplace=True)
        aligned_pred = df_forecast.reindex(df_actual.index)['yhat'].fillna(method='ffill')
        models_forecasts[model_name] = aligned_pred

    results = ForecastEvaluator.compare_models(models_forecasts, df_actual[actual_column])
    return results
