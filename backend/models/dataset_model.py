# Neurolytix\backend\models\dataset_model.py

from sqlalchemy import Column, String, Integer, DateTime, func
from database.db import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(String, nullable=True)  # Can link to user id
