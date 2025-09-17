# Neurolytix\backend\utils/validators.py

import pandas as pd

def validate_dataset_columns(df: pd.DataFrame, required_columns: list):
    """
    Ensure all required columns exist in the dataframe.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return True

def validate_forecast_horizon(horizon: int, max_horizon: int = 365):
    """
    Validate the forecast horizon is within acceptable limits.
    """
    if horizon <= 0:
        raise ValueError("Horizon must be greater than 0.")
    if horizon > max_horizon:
        raise ValueError(f"Horizon cannot exceed {max_horizon} periods.")
    return True
