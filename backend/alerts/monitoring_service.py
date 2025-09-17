# Neurolytix\backend\alerts\monitoring_service.py

from apscheduler.schedulers.background import BackgroundScheduler
from routers.alerts import alert_anomalies
import logging

logger = logging.getLogger(__name__)

class MonitoringService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = []

    def start(self):
        self.scheduler.start()
        logger.info("Monitoring service started")

    def schedule_anomaly_check(self, dataset_id, target_column, user_email, cron_expr="0 * * * *"):
        """
        Schedule anomaly detection based on cron expression
        Default: every hour at minute 0
        """
        job = self.scheduler.add_job(
            func=alert_anomalies,
            trigger='cron',
            minute='0',  # default hourly
            args=[dataset_id, target_column, user_email],
            id=f"anomaly_{dataset_id}_{target_column}",
            replace_existing=True
        )
        self.jobs.append(job)
        logger.info(f"Scheduled anomaly check for {dataset_id} - {target_column}")
