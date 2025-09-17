# backend/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if available)
load_dotenv()

class Config:
    # 🔹 App settings
    APP_NAME = "Neurolytix"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # 🔹 Data directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    FORECAST_DIR = os.path.join(DATA_DIR, "forecasts")
    CLUSTER_DIR = os.path.join(DATA_DIR, "clusters")
    ANOMALY_DIR = os.path.join(DATA_DIR, "anomalies")

    # Ensure directories exist
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(FORECAST_DIR, exist_ok=True)
    os.makedirs(CLUSTER_DIR, exist_ok=True)
    os.makedirs(ANOMALY_DIR, exist_ok=True)

    # 🔹 Database config (future-proofing)
    DB_URL = os.getenv("DATABASE_URL", "sqlite:///backend/data/neurolytix.db")

    # 🔹 Security (placeholder for API keys)
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    # 🔹 AI/ML settings
    FORECAST_HORIZON = int(os.getenv("FORECAST_HORIZON", "10"))  # default 10 steps
    CLUSTER_DEFAULT_K = int(os.getenv("CLUSTER_DEFAULT_K", "3"))
    ANOMALY_THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", "0.05"))

