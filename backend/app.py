# Neurolytix\backend\app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers directly (no 'backend.' prefix)
from routers import datasets, analysis, forecasting, visualization, auth, clustering

app = FastAPI(
    title="Neurolytix - AI-Powered Data Analytics",
    description="A futuristic data analytics and forecasting platform for global companies",
    version="0.1.0"
)

# Include clustering router first
app.include_router(clustering.router, prefix="/api", tags=["Clustering"])

# Enable CORS (for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include other routers
app.include_router(datasets.router, prefix="/api/datasets", tags=["Datasets"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(forecasting.router, prefix="/api/forecasting", tags=["Forecasting"])
app.include_router(visualization.router, prefix="/api/visualization", tags=["Visualization"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Welcome to Neurolytix - AI-Powered Data Analytics"}

if __name__ == "__main__":
    import uvicorn
    # Run uvicorn pointing to app:app since we're inside backend/
    uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)
