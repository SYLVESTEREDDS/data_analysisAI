# Neurolytix\backend\routers\analysis.py

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import os
import pandas as pd

router = APIRouter()

DATA_DIR = "Neurolytix/backend/data/raw"

@router.get("/profile")
def profile_dataset(dataset_id: str = Query(..., description="Dataset ID")):
    """
    Generate basic profile and descriptive statistics for a dataset.
    """
    try:
        # Find the file by dataset_id
        files = os.listdir(DATA_DIR)
        dataset_file = None
        for f in files:
            if f.startswith(dataset_id):
                dataset_file = os.path.join(DATA_DIR, f)
                break

        if not dataset_file:
            raise HTTPException(status_code=404, detail="Dataset not found.")

        # Load the dataset
        if dataset_file.endswith(".csv"):
            df = pd.read_csv(dataset_file)
        elif dataset_file.endswith((".xlsx", ".xls")):
            df = pd.read_excel(dataset_file)
        elif dataset_file.endswith(".json"):
            df = pd.read_json(dataset_file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        # Generate summary statistics
        summary = df.describe(include="all").to_dict()
        missing_values = df.isnull().sum().to_dict()
        num_rows, num_cols = df.shape
        columns = df.columns.tolist()
        dtypes = df.dtypes.astype(str).to_dict()

        return JSONResponse(
            status_code=200,
            content={
                "dataset_id": dataset_id,
                "filename": os.path.basename(dataset_file),
                "num_rows": num_rows,
                "num_columns": num_cols,
                "columns": columns,
                "dtypes": dtypes,
                "missing_values": missing_values,
                "summary_statistics": summary
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to profile dataset: {str(e)}")
