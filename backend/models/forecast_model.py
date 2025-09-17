# Neurolytix\backend\models\forecast_model.py

from sqlalchemy import Column, String, Integer, DateTime, JSON, func
from database.db import Base

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, nullable=False)
    target_column = Column(String, nullable=False)
    horizon = Column(Integer, nullable=False)
    forecast_data = Column(JSON, nullable=False)  # Stores predicted values
    created_at = Column(DateTime(timezone=True), server_default=func.now())
