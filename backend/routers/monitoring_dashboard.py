from fastapi import APIRouter
from alerts.monitoring_service import monitoring_service
import os
import pandas as pd

router = APIRouter()
ALERTS_DIR = "Neurolytix/backend/data/alerts"
os.makedirs(ALERTS_DIR, exist_ok=True)

@router.get("/active_jobs")
def get_active_jobs():
    jobs = monitoring_service.jobs
    job_list = [
        {
            "id": job.id,
            "next_run_time": str(job.next_run_time),
            "args": job.args
        }
        for job in jobs
    ]
    return job_list

@router.get("/recent_alerts")
def get_recent_alerts(limit: int = 10):
    alerts_files = sorted(os.listdir(ALERTS_DIR), reverse=True)[:limit]
    alerts_data = []
    for file in alerts_files:
        path = os.path.join(ALERTS_DIR, file)
        df = pd.read_csv(path)
        alerts_data.extend(df.to_dict(orient="records"))
    return alerts_data
