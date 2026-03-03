from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers.detect_fraud_router import router
from app.services.detect_fraud_service import PredictionError

from dotenv import load_dotenv

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


@app.get("/")
def home():
    return {"message": "FraudDetect - A High Level Fraud Detection System"}


app.include_router(router)