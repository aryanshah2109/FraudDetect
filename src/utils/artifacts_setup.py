import json
import os
from datetime import datetime
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

from src.config import config_loader
from src.logger import logging

class ArtifactsSetup:
    """
    Used to setup artifacts directory    
    """
    
    def __init__(self):
        config = config_loader.load_config()

        self.model_name = config["model"]["name"]
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.artifact_path: Path = (
            Path("artifacts") 
            / self.model_name
            / self.timestamp
        )

        self.artifact_path.mkdir(parents=True, exist_ok=True)

        logging.info(f"Artifacts directory created at {self.artifact_path}")

        self.artifacts_plots_path = self.artifact_path / "plots"
        self.artifacts_plots_path.mkdir(parents=True, exist_ok=True)

    
    def save_pipeline(self, pipeline, filename):
        try:
            file_path = Path(self.artifact_path) / f"{filename}.pkl"
            joblib.dump(pipeline, file_path)
        except:
            logging.error(f"Error while saving pipeline to {self.artifact_path}")
            raise
    
    def save_csv_artifact(self, df: pd.DataFrame, filename):
        try:
            file_path = Path(self.artifact_path) / f"{filename}.csv"
            df.to_csv(file_path, index=False)
        except:
            logging.error(f"Error while saving dataframe to {self.artifact_path}")
            raise

    def save_model(self, model, filename="model.pkl"):
        try:
            file_path = Path(self.artifact_path) / filename
            joblib.dump(model, file_path)
        except:
            logging.error(f"Error while saving model to {self.artifact_path}")
            raise
    
    def save_json(self, data: dict, filename):
        try:
            file_path = Path(self.artifact_path) / filename

            # Convert numpy types to native Python types
            def convert(o):
                if isinstance(o, (np.integer,)):
                    return int(o)
                if isinstance(o, (np.floating,)):
                    return float(o)
                if isinstance(o, (np.ndarray,)):
                    return o.tolist()
                return o

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4, default=convert)

        except Exception as e:
            logging.error(f"Error while saving json object to {self.artifact_path}: {e}")
            raise