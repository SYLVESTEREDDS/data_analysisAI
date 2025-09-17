from fastapi import FastAPI
from alerts.monitoring_service import MonitoringService

app = FastAPI()

monitoring_service = MonitoringService()
monitoring_service.start()

# Example: Schedule dataset anomaly checks
monitoring_service.schedule_anomaly_check(
    dataset_id="dataset123",
    target_column="sales",
    user_email="user@example.com"
)
