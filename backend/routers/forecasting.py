# Neurolytix\backend\routers\forecasting.py

from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse
import os
import pandas as pd
from io import StringIO

from services.forecasting_engine import ForecastingEngine
from forecasting.lstm_forecast import LSTMForecaster
from forecasting.ensemble import EnsembleForecaster
from forecasting.deep_hybrid import DeepHybridForecaster
from services.forecast_service import ForecastService
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

DATA_DIR = "Neurolytix/backend/data/raw"
FORECAST_DIR = "Neurolytix/backend/data/forecasts"
os.makedirs(FORECAST_DIR, exist_ok=True)

forecast_engine = ForecastingEngine()
forecast_service = ForecastService()


@router.get("/predict")
def forecast_dataset(
    dataset_id: str = Query(..., description="Dataset ID"),
    target_column: str = Query(..., description="Column to forecast"),
    horizon: int = Query(30, description="Number of future periods to predict"),
    method: str = Query("default", description="Forecasting method: 'default' or 'lstm'")
):
    """
    Generate forecasts for a specified dataset and target column.
    Supports 'default' (ForecastingEngine) and 'lstm' (LSTMForecaster) methods.
    """
    try:
        files = os.listdir(DATA_DIR)
        dataset_file = next((f for f in files if f.startswith(dataset_id)), None)

        if not dataset_file:
            raise HTTPException(status_code=404, detail="Dataset not found.")

        dataset_path = os.path.join(DATA_DIR, dataset_file)
        if dataset_file.endswith(".csv"):
            df = pd.read_csv(dataset_path)
        elif dataset_file.endswith((".xlsx", ".xls")):
            df = pd.read_excel(dataset_path)
        elif dataset_file.endswith(".json"):
            df = pd.read_json(dataset_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        if target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target column '{target_column}' not found.")

        if method == "lstm":
            # Preprocess for LSTM
            df[target_column] = pd.to_numeric(df[target_column], errors='coerce')
            df.dropna(subset=[target_column], inplace=True)
            if 'ds' not in df.columns:
                raise HTTPException(status_code=400, detail="Column 'ds' (datetime) not found for LSTM method.")
            df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
            df.dropna(subset=['ds'], inplace=True)
            df.set_index('ds', inplace=True)
            series = df[target_column]

            lstm = LSTMForecaster(sequence_length=30, epochs=50)
            lstm.fit(series)
            forecast = lstm.predict(series, horizon=horizon)
            forecast_result = forecast.to_dict(orient='records')
        else:
            # Use default forecasting engine
            forecast_result = forecast_engine.forecast(df, target_column, horizon=horizon)

        return JSONResponse(
            status_code=200,
            content={
                "dataset_id": dataset_id,
                "target_column": target_column,
                "horizon": horizon,
                "method": method,
                "forecast": forecast_result
            }
        )

    except Exception as e:
        logger.error(f"Forecasting failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Forecasting failed: {str(e)}")


@router.get("/ensemble_predict")
def ensemble_predict(
    dataset_id: str = Query(..., description="Dataset ID"),
    target_column: str = Query(..., description="Column to forecast"),
    horizon: int = Query(30, description="Number of future periods to predict")
):
    """
    Generate ensemble forecasts for a specified dataset and target column.
    Uses EnsembleForecaster with predefined weights.
    """
    try:
        files = os.listdir(DATA_DIR)
        dataset_file = next((f for f in files if f.startswith(dataset_id)), None)
        if not dataset_file:
            raise HTTPException(status_code=404, detail="Dataset not found.")

        dataset_path = os.path.join(DATA_DIR, dataset_file)
        if dataset_file.endswith(".csv"):
            df = pd.read_csv(dataset_path)
        elif dataset_file.endswith((".xlsx", ".xls")):
            df = pd.read_excel(dataset_path)
        elif dataset_file.endswith(".json"):
            df = pd.read_json(dataset_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        if target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{target_column}' not in dataset.")

        df[target_column] = pd.to_numeric(df[target_column], errors='coerce')
        df.dropna(subset=[target_column], inplace=True)
        if 'ds' not in df.columns:
            raise HTTPException(status_code=400, detail="Column 'ds' (datetime) not found in dataset.")
        df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
        df.dropna(subset=['ds'], inplace=True)

        ensemble = EnsembleForecaster(weights={"lstm": 0.6, "prophet": 0.4})
        ensemble.fit(df, target_column)
        forecast = ensemble.predict(df, target_column, horizon=horizon)
        forecast_result = forecast.to_dict(orient='records')

        return JSONResponse(
            status_code=200,
            content={
                "dataset_id": dataset_id,
                "target_column": target_column,
                "horizon": horizon,
                "method": "ensemble",
                "forecast": forecast_result
            }
        )

    except Exception as e:
        logger.error(f"Ensemble forecasting failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Forecasting failed: {str(e)}")


@router.get("/deep_predict")
def deep_predict(
    dataset_id: str = Query(..., description="Dataset ID"),
    target_column: str = Query(..., description="Column to forecast"),
    horizon: int = Query(30, description="Number of future periods to predict"),
    lstm_sequence_length: int = Query(30),
    lstm_epochs: int = Query(50),
    lstm_batch_size: int = Query(32),
    prophet_daily: bool = Query(True),
    prophet_weekly: bool = Query(True),
    prophet_yearly: bool = Query(True),
    changepoint_prior_scale: float = Query(0.05),
    save: bool = Query(True),
):
    """
    Prophet + LSTM(residual) hybrid.
    Requires dataset with columns ['ds', target_column].
    """
    try:
        files = os.listdir(DATA_DIR)
        dataset_file = next((f for f in files if f.startswith(dataset_id)), None)
        if not dataset_file:
            raise HTTPException(status_code=404, detail="Dataset not found.")

        df = pd.read_csv(os.path.join(DATA_DIR, dataset_file))
        if target_column not in df.columns:
            raise HTTPException(
                status_code=400, detail=f"Column {target_column} not in dataset."
            )

        df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
        df[target_column] = pd.to_numeric(df[target_column], errors="coerce")
        df.dropna(subset=["ds", target_column], inplace=True)
        df = df.sort_values("ds")

        model = DeepHybridForecaster(
            lstm_sequence_length=lstm_sequence_length,
            lstm_epochs=lstm_epochs,
            lstm_batch_size=lstm_batch_size,
            prophet_daily=prophet_daily,
            prophet_weekly=prophet_weekly,
            prophet_yearly=prophet_yearly,
            prophet_changepoint_prior_scale=changepoint_prior_scale,
        )

        logger.info("Fitting Deep Hybrid forecaster…")
        model.fit(df, target_column)
        forecast = model.predict(df, target_column, horizon=horizon)

        # Optionally save
        if save:
            out_name = f"{dataset_id}_deep_hybrid.csv"
            out_path = os.path.join(FORECAST_DIR, out_name)
            forecast.to_csv(out_path, index=False)
            logger.info(f"Saved deep hybrid forecast to {out_path}")

        return JSONResponse(
            status_code=200,
            content={
                "dataset_id": dataset_id,
                "target_column": target_column,
                "horizon": horizon,
                "method": "deep_hybrid",
                "forecast": forecast.to_dict(orient="records"),
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Deep Hybrid forecasting failed.")
        raise HTTPException(status_code=500, detail=f"Forecasting failed: {str(e)}")


@router.post("/forecast/")
async def generate_forecast(
    file: UploadFile = File(...), 
    column: str = None, 
    periods: int = 10
):
    """
    Upload dataset and generate forecast for a given column.
    Args:
        file: CSV file containing time-series or numeric data
        column: The column to forecast
        periods: Number of future periods to predict
    """
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

        if column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{column}' not found in dataset")

        forecast_df = forecast_service.make_forecast(df, column, periods)

        return {
            "status": "success",
            "message": f"Forecast generated for column '{column}'",
            "forecast": forecast_df.to_dict(orient="records")
        }
    except Exception as e:
        logger.error(f"Upload-based forecasting failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
