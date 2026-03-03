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

            config = config_loader.load_config()
            current_schema_version = config["schema"]["version"]

            artifacts_dir = Path("artifacts") / self.model_name

            best_score = float("-inf")
            best_model_path = None
            best_preprocessor_path = None
            best_metrics_path = None
            best_run_folder = None

            for run_name in artifacts_dir.iterdir():
                if run_name.is_dir():
                    metrics_path = run_name / "metrics.json"

                    if not metrics_path.exists():
                        continue

                    if metrics_path.stat().st_size == 0:
                        logging.warning(f"Skipping empty metrics file: {metrics_path}")
                        continue

                    try:
                        with open(metrics_path, "r") as file:
                            metrics = json.load(file)
                    except json.JSONDecodeError:
                        logging.warning(f"Skipping corrupted metrics file: {metrics_path}")
                        continue

                    run_schema_version = metrics.get("schema_version")

                    # Skip incompatible schema versions
                    if run_schema_version != current_schema_version:
                        logging.info(
                            f"Skipping run {run_name.name} due to schema mismatch "
                            f"(run: {run_schema_version}, current: {current_schema_version})"
                        )
                        continue

                    recall = metrics.get("recall")
                    pr_auc = metrics.get("pr_auc")

                    if recall is None or pr_auc is None:
                        continue

                    # enforce minimum recall
                    if recall < 0.70:
                        continue

                    score = pr_auc

                    if score is not None and score > best_score:
                        best_score = score
                        best_model_path = run_name / f"{self.model_name}_model.pkl"
                        best_preprocessor_path = run_name / "preprocessor.pkl"
                        best_metrics_path = run_name / "metrics.json"
                        best_run_folder = run_name

            if best_model_path is None:
                raise ValueError(
                    f"No compatible models found for schema version {current_schema_version}"
                )

            logging.info(f"Best run name: {best_run_folder}")
            logging.info(f"Best metric on which model is chosen: {best_score}")

            model = joblib.load(best_model_path)
            preprocessor = joblib.load(best_preprocessor_path)
            with open(best_metrics_path, "r") as f:
                metrics = json.load(f)

            final_model_path = Path("models") / "best_model.pkl"
            final_preprocessor_path = Path("models") / "best_preprocessor.pkl"
            final_metrics_path = Path("models") / "best_metrics.json"

            final_model_path.parent.mkdir(parents=True, exist_ok=True)

            joblib.dump(model, final_model_path)
            joblib.dump(preprocessor, final_preprocessor_path)

            with open(final_metrics_path, "w") as f:
                json.dump(metrics, f, indent=4)

            logging.info(f"Best model stored at {final_model_path}")
            logging.info(f"Best preprocessor stored at {final_preprocessor_path}")
            logging.info(f"Best metrics stored at {final_metrics_path}")

        except Exception as e:
            logging.error(f"Error selecting best model: {e}")
            raise