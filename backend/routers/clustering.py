from fastapi import APIRouter, UploadFile, File, Form
import pandas as pd
from services.clustering_service import ClusteringService
from io import StringIO

router = APIRouter()

@router.post("/cluster/")
async def cluster_dataset(file: UploadFile = File(...), n_clusters: int = Form(...), method: str = Form("kmeans")):
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        return {"error": f"Failed to read CSV: {str(e)}"}

    clustering = ClusteringService(df)

    if method.lower() == "kmeans":
        clusters = clustering.kmeans(n_clusters)
    elif method.lower() == "agglomerative":
        clusters = clustering.agglomerative(n_clusters)
    else:
        return {"error": "Invalid clustering method"}

    return {"clusters": clusters, "columns": df.columns.tolist(), "n_clusters": n_clusters, "method": method}
