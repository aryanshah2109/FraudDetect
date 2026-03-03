from pathlib import Path
import joblib
import json

from src.config import config_loader

config = config_loader.load_config()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / config["inference"]["best_model_path"]
PREPROCESSOR_PATH = BASE_DIR / config["inference"]["best_preprocessor_path"]
METRICS_PATH = BASE_DIR / config["inference"]["best_metrics_path"]



print("Loading model...")
model = joblib.load(MODEL_PATH)
print("Model loaded")

print("Loading preprocessor...")
preprocessor = joblib.load(PREPROCESSOR_PATH)
print("Preprocessor loaded")

with open(METRICS_PATH, "r") as file:
    metrics = json.load(file)