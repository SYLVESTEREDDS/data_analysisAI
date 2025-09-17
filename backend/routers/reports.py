from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

router = APIRouter()

DATA_DIR = "Neurolytix/backend/data/raw"
FORECAST_DIR = "Neurolytix/backend/data/forecasts"
REPORT_DIR = "Neurolytix/backend/data/reports"

os.makedirs(REPORT_DIR, exist_ok=True)

@router.get("/download_forecast_csv")
def download_forecast_csv(forecast_file: str = Query(...)):
    path = os.path.join(FORECAST_DIR, forecast_file)
    if not os.path.exists(path):
        return {"error": "Forecast file not found"}
    return FileResponse(path, media_type="text/csv", filename=forecast_file)

@router.get("/generate_forecast_pdf")
def generate_forecast_pdf(forecast_file: str = Query(...)):
    path = os.path.join(FORECAST_DIR, forecast_file)
    if not os.path.exists(path):
        return {"error": "Forecast file not found"}

    df = pd.read_csv(path)
    pdf_file = os.path.join(REPORT_DIR, f"{forecast_file.replace('.csv','')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Forecast Report: {forecast_file}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for idx, row in df.iterrows():
        line = ", ".join([f"{col}: {row[col]}" for col in df.columns])
        pdf.multi_cell(0, 8, line)

    pdf.output(pdf_file)
    return FileResponse(pdf_file, media_type="application/pdf", filename=os.path.basename(pdf_file))
