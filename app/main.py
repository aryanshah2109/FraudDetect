from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers.artifacts_router import router as artifacts_router
from app.routers.detect_fraud_router import router as detect_router
from app.services.detect_fraud_service import PredictionError
from app.core.config import load_artifacts, BASE_DIR

import warnings
warnings.filterwarnings("ignore")

load_dotenv()


app = FastAPI(title="FraudDetect")


# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Global Exception Handler
@app.exception_handler(PredictionError)
async def prediction_exception_handler(request: Request, exc: PredictionError):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Model Inference Failed",
            "detail": str(exc)
        }
    )

@app.on_event("startup")
def load_model():
    load_artifacts()

@app.get("/")
def home():
    return {"message": "FraudDetect - A High Level Fraud Detection System"}


app.mount("/artifacts/files", StaticFiles(directory=BASE_DIR / "artifacts"), name="artifact_files")
app.include_router(detect_router)
app.include_router(artifacts_router)