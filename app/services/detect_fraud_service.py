from pathlib import Path
import json
import pandas as pd

from app.core.config import model, preprocessor
from app.schemas.detect_fraud_schema import (
    DetectFraudRequest,
    DetectFraudResponse
)
from src.config import config_loader
from src.logger import logging


class PredictionError(Exception):
    pass


class ThresholdFetcher:
    def __init__(self):
        config = config_loader.load_config()
        self.best_metrics_path = Path(config["inference"]["best_metrics_path"])

    def get_threshold(self) -> float:
        try:
            logging.info("Fetching best threshold value")
            with open(self.best_metrics_path, "r") as file:
                metrics = json.load(file)

            return metrics["threshold"]

        except Exception as e:
            logging.error(f"Could not fetch best threshold value: {e}")
            raise PredictionError("Failed to load threshold value.")


class FraudDetectionService:

    def __init__(self):
        self.threshold = ThresholdFetcher().get_threshold()

    def predict(self, payload: DetectFraudRequest) -> DetectFraudResponse:
        try:
            # Convert to dict (JSON mode auto-converts Enum)
            data = payload.model_dump(mode="json")

            # Convert to DataFrame
            input_df = pd.DataFrame([data])

            # Preprocess
            processed_data = preprocessor.transform(input_df)

            # Get probability of fraud (class 1)
            probability = model.predict_proba(processed_data)[0][1]

            # Apply trained threshold
            prediction = int(probability >= self.threshold)

            return DetectFraudResponse(
                prediction=prediction,
                prediction_label="Fraud" if prediction else "Not Fraud",
                fraud_probability=probability
            )

        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise PredictionError("Model inference failed.")


# Singleton instance
fraud_detection_service = FraudDetectionService()