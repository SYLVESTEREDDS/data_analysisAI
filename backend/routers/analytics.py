from fastapi import APIRouter, Query, HTTPException
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

router = APIRouter()

DATA_DIR = "data/uploads"


@router.get("/summary_stats/")
def summary_stats(filename: str = Query(...)):
    """
    Generate summary statistics for a dataset.
    """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = pd.read_csv(file_path)
        stats = df.describe(include="all").to_dict()
        return {"filename": filename, "summary": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary stats: {str(e)}")


@router.get("/correlation/")
def correlation(filename: str = Query(...)):
    """
    Compute correlation matrix for numerical columns.
    """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = pd.read_csv(file_path)
        corr = df.corr(numeric_only=True).to_dict()
        return {"filename": filename, "correlation_matrix": corr}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating correlation: {str(e)}")


@router.get("/cluster/")
def cluster(filename: str = Query(...), n_clusters: int = 3):
    """
    Apply KMeans clustering to dataset (numerical columns only).
    """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = pd.read_csv(file_path)
        numeric_df = df.select_dtypes(include=["number"]).dropna()

        if numeric_df.empty:
            raise HTTPException(status_code=400, detail="No numeric columns available for clustering")

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_df)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df["cluster"] = kmeans.fit_predict(scaled_data)

        return {
            "filename": filename,
            "clusters": df["cluster"].value_counts().to_dict(),
            "sample_with_clusters": df.head(10).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing clustering: {str(e)}")
