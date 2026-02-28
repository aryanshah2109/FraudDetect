import json
import os
from datetime import datetime
from pathlib import Path
import joblib
import pandas as pd

from src.config import config_loader
from src.logger import logging

class ArtifactsSetup:
    """
    Used to setup artifacts directory    
    """
    
    def __init__(self):
        config = config_loader.load_config()

        self.model_name = config["model"]["name"]

    def get_artifact_dir_name(self):
        """
        Fetches artifact directory name based on timestamp and model name
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.artifact_path: Path = (
            Path("artifacts") 
            / self.model_name
            / timestamp
        )

        self.artifact_path.mkdir(parents=True, exist_ok=True)

        logging.info(f"Artifacts directory created at {self.artifact_path}")

        return self.artifact_path
    
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
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
        except:
            logging.error(f"Error while saving json object to {self.artifact_path}")
            raise

