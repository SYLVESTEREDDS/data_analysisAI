# Neurolytix\backend\routers\visualization.py

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import os
import pandas as pd

router = APIRouter()

DATA_DIR = "Neurolytix/backend/data/raw"

@router.get("/line_plot")
def line_plot(dataset_id: str = Query(..., description="Dataset ID"), 
              columns: str = Query(..., description="Comma-separated columns to plot")):
    """
    Returns data for line plot visualization for selected columns.
    Frontend can use this for interactive charts.
    """
    try:
        # Locate the dataset
        files = os.listdir(DATA_DIR)
        dataset_file = None
        for f in files:
            if f.startswith(dataset_id):
                dataset_file = os.path.join(DATA_DIR, f)
                break

        if not dataset_file:
            raise HTTPException(status_code=404, detail="Dataset not found.")

        # Load dataset
        if dataset_file.endswith(".csv"):
            df = pd.read_csv(dataset_file)
        elif dataset_file.endswith((".xlsx", ".xls")):
            df = pd.read_excel(dataset_file)
        elif dataset_file.endswith(".json"):
            df = pd.read_json(dataset_file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        # Columns to plot
        plot_columns = [col.strip() for col in columns.split(",")]
        for col in plot_columns:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Column '{col}' not found in dataset.")

        # Ensure 'ds' column exists for x-axis
        if 'ds' not in df.columns:
            raise HTTPException(status_code=400, detail="Dataset must contain a 'ds' column for datetime.")

        # Prepare data
        plot_data = []
        for col in plot_columns:
            series = [{"x": str(date), "y": value} for date, value in zip(df['ds'], df[col])]
            plot_data.append({"column": col, "series": series})

        return JSONResponse(
            status_code=200,
            content={
                "dataset_id": dataset_id,
                "plot_data": plot_data
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization data generation failed: {str(e)}")
