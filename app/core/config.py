import json
from pathlib import Path

import joblib

from src.config import config_loader

config = config_loader.load_config()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / config["inference"]["best_model_path"]
PREPROCESSOR_PATH = BASE_DIR / config["inference"]["best_preprocessor_path"]
METRICS_PATH = BASE_DIR / config["inference"]["best_metrics_path"]

model = None
preprocessor = None


def load_artifacts():
    global model, preprocessor

    if model is None:
        print("Loading model...")
        model = joblib.load(MODEL_PATH)

    if preprocessor is None:
        print("Loading preprocessor...")
        preprocessor = joblib.load(PREPROCESSOR_PATH)

    return model, preprocessor