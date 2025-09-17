from fastapi import APIRouter, Query, HTTPException
import os
import pandas as pd
from analytics.anomaly_detection import AnomalyDetector

router = APIRouter()

# Directories
FORECAST_DIR = "Neurolytix/backend/data/forecasts"
RAW_DATA_DIR = "Neurolytix/backend/data/raw"
UPLOADS_DIR = "data/uploads"


@router.get("/forecast_visualization")
def forecast_visualization(dataset_id: str = Query(...), actual_column: str = Query(...)):
    """
    Visualize actual data against model forecasts.
    """
    # Load actual dataset
    dataset_file = next((f for f in os.listdir(RAW_DATA_DIR) if f.startswith(dataset_id)), None)
    if not dataset_file:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df_actual = pd.read_csv(os.path.join(RAW_DATA_DIR, dataset_file))
    if actual_column not in df_actual.columns:
        raise HTTPException(status_code=400, detail=f"Column '{actual_column}' not found")

    df_actual['ds'] = pd.to_datetime(df_actual['ds'], errors='coerce')
    df_actual[actual_column] = pd.to_numeric(df_actual[actual_column], errors='coerce')
    df_actual.dropna(subset=['ds', actual_column], inplace=True)

    # Load forecast models
    model_files = [f for f in os.listdir(FORECAST_DIR) if f.startswith(dataset_id)]
    forecasts = {}
    for file in model_files:
        model_name = file.replace(f"{dataset_id}_", "").replace(".csv", "")
        df_forecast = pd.read_csv(os.path.join(FORECAST_DIR, file))
        df_forecast['ds'] = pd.to_datetime(df_forecast['ds'], errors='coerce')
        df_forecast['yhat'] = pd.to_numeric(df_forecast['yhat'], errors='coerce')
        df_forecast.dropna(subset=['ds', 'yhat'], inplace=True)
        df_forecast.set_index('ds', inplace=True)

        aligned_pred = df_forecast.reindex(df_actual['ds'])['yhat'].fillna(method='ffill')
        forecasts[model_name] = aligned_pred.tolist()

    return {
        "dates": df_actual['ds'].dt.strftime('%Y-%m-%d').tolist(),
        "actual": df_actual[actual_column].tolist(),
        "forecasts": forecasts
    }


@router.get("/histogram/")
def histogram(filename: str = Query(...), column: str = Query(...), bins: int = 10):
    """
    Generate histogram data for a given column.
    """
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = pd.read_csv(file_path)
        if column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{column}' not found")

        counts, bin_edges = pd.cut(df[column].dropna(), bins=bins, retbins=True)
        histogram_data = pd.value_counts(counts, sort=False).to_dict()

        return {
            "filename": filename,
            "column": column,
            "bins": bin_edges.tolist(),
            "counts": list(histogram_data.values())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating histogram: {str(e)}")


@router.get("/lineplot/")
def lineplot(filename: str = Query(...), x_column: str = Query(...), y_column: str = Query(...)):
    """
    Generate line plot data for two columns.
    """
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = pd.read_csv(file_path)
        if x_column not in df.columns or y_column not in df.columns:
            raise HTTPException(status_code=400, detail="Invalid columns provided")

        data = df[[x_column, y_column]].dropna().to_dict(orient="records")

        return {
            "filename": filename,
            "x_column": x_column,
            "y_column": y_column,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating line plot: {str(e)}")


@router.get("/scatterplot/")
def scatterplot(filename: str = Query(...), x_column: str = Query(...), y_column: str = Query(...)):
    """
    Generate scatter plot data for two columns.
    """
    file_path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = pd.read_csv(file_path)
        if x_column not in df.columns or y_column not in df.columns:
            raise HTTPException(status_code=400, detail="Invalid columns provided")

        data = df[[x_column, y_column]].dropna().to_dict(orient="records")

        return {
            "filename": filename,
            "x_column": x_column,
            "y_column": y_column,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating scatter plot: {str(e)}")
