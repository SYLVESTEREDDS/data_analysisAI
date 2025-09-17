# Neurolytix\backend\routers\datasets.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import pandas as pd
from io import StringIO
from utils import file_handler

router = APIRouter()

# Directory to store uploaded datasets
DATA_DIR = "Neurolytix/backend/data/raw"
os.makedirs(DATA_DIR, exist_ok=True)


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a dataset (CSV, Excel, JSON).
    Returns dataset ID, filename, and column names if applicable.
    """
    try:
        # Generate a unique ID for the dataset
        dataset_id = str(uuid.uuid4())
        filename = f"{dataset_id}_{file.filename}"
        file_path = os.path.join(DATA_DIR, filename)

        # Save the uploaded file
        await file_handler.save_upload(file, file_path)

        # Try reading file if CSV/Excel/JSON to extract metadata
        columns = []
        try:
            if file.filename.endswith(".csv"):
                df = pd.read_csv(file_path)
                columns = df.columns.tolist()
            elif file.filename.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file_path)
                columns = df.columns.tolist()
            elif file.filename.endswith(".json"):
                df = pd.read_json(file_path)
                columns = df.columns.tolist()
        except Exception:
            pass  # Ignore parsing errors, still store file

        return JSONResponse(
            status_code=200,
            content={
                "dataset_id": dataset_id,
                "filename": file.filename,
                "columns": columns,
                "message": "Dataset uploaded successfully."
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/list")
def list_datasets():
    """
    List all uploaded datasets with their IDs and file names.
    """
    try:
        files = os.listdir(DATA_DIR)
        datasets = [
            {
                "dataset_id": f.split("_")[0],
                "filename": "_".join(f.split("_")[1:])
            }
            for f in files
        ]
        return {"datasets": datasets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list datasets: {str(e)}")


@router.get("/get_dataset/{dataset_id}")
def get_dataset(dataset_id: str):
    """
    Retrieve dataset details by dataset ID.
    Returns filename, row/column count, and sample data.
    """
    try:
        # Find the file with this dataset_id
        matching_files = [f for f in os.listdir(DATA_DIR) if f.startswith(dataset_id)]
        if not matching_files:
            raise HTTPException(status_code=404, detail="Dataset not found")

        file_path = os.path.join(DATA_DIR, matching_files[0])
        filename = "_".join(matching_files[0].split("_")[1:])

        # Load file based on extension
        if filename.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        elif filename.endswith(".json"):
            df = pd.read_json(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        return {
            "dataset_id": dataset_id,
            "filename": filename,
            "rows": len(df),
            "columns": df.columns.tolist(),
            "sample": df.head(10).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading dataset: {str(e)}")
