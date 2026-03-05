from fastapi import APIRouter

from app.schemas.detect_fraud_schema import (DetectFraudRequest,
                                             DetectFraudResponse)
from app.services.detect_fraud_service import fraud_detection_service

router = APIRouter(
    prefix="/predict",
    tags=["prediction"]
)


@router.post("/", response_model=DetectFraudResponse)
async def predict(payload: DetectFraudRequest):
    return fraud_detection_service.predict(payload)