import joblib
import json
from pathlib import Path

from src.logger import logging
from src.utils.artifacts_setup import ArtifactsSetup
from src.config import config_loader

class ModelPicker:
    """
    Picks the best model based on recall score from artifacts
    """
    def __init__(self, artifacts_object: ArtifactsSetup, metric: str):
        config = config_loader.load_config()
        self.model_name = config["model"]["name"]
        self.metric = metric
        self.artifacts_path = artifacts_object.artifact_path
        self.best_model_path = Path("models")

    def pick_best_model(self):
        try:
            logging.info("Picking best model and storing in models/ folder")        
            logging.info(f"Metric chosen: {self.metric}")
            artifacts_dir = Path("artifacts") / self.model_name

            best_score = float("-inf")
            best_model_path = None
            best_run_folder = None

            for run_name in artifacts_dir.iterdir():
                if run_name.is_dir():
                    metrics_path = run_name / "metrics.json"

                    # Skip if file doesn't exist
                    if not metrics_path.exists():
                        continue

                    # Skip empty files
                    if metrics_path.stat().st_size == 0:
                        logging.warning(f"Skipping empty metrics file: {metrics_path}")
                        continue

                    try:
                        with open(metrics_path, "r") as file:
                            metrics = json.load(file)
                    except json.JSONDecodeError:
                        logging.warning(f"Skipping corrupted metrics file: {metrics_path}")
                        continue

                    score = metrics.get(self.metric)

                    if score is not None and score > best_score:
                        best_score = score
                        best_model_path = run_name / f"{self.model_name}_model.pkl"
                        best_run_folder = run_name

            if best_model_path is None:
                logging.error("No models found to pick from")
                raise

            logging.info(f"Best run name: {best_run_folder}")
            logging.info(f"Best metric on which model is chosen: {best_score}")

            model = joblib.load(best_model_path)

            final_model_path = Path("models") / "best_model.pkl"
            final_model_path.parent.mkdir(parents=True, exist_ok=True)

            joblib.dump(model, final_model_path)

            logging.info(f"Best model stored at {final_model_path}")

            logging.info(f"Best model chosen and stored at {self.best_model_path}")


        except Exception as e:
            logging.error(f"Error selecting best model on: {e}")
            raise
