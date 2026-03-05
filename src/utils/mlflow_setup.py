import mlflow
from dotenv import load_dotenv

from src.config import config_loader
from src.logger import logging
from src.utils.artifacts_setup import ArtifactsSetup

load_dotenv()  

class MLFlowSetup:
    """
    Manages MLflow experiment tracking: sets up tracking URI, experiment, and logging operations
    """

    def __init__(self, artifacts_setup: ArtifactsSetup):
        logging.debug("Initializing MLFlow setup")
        config = config_loader.load_config()

        self.artifacts_setup = artifacts_setup
        self.artifacts_path = self.artifacts_setup.artifact_path

        self.model_name = config["model"]["name"]

        self.tracking_uri = config["mlflow"]["mlflow_tracking_uri"]
        self.experiment_name = config["mlflow"]["experiment_name"]        

        mlflow.set_tracking_uri(self.tracking_uri)
        logging.debug(f"MLFlow tracking URI set to: {self.tracking_uri}")
        
        mlflow.set_experiment(self.experiment_name)
        logging.debug(f"MLFlow experiment set to: {self.experiment_name}")

    def get_run_name(self):
        run_name = f"{self.model_name}_{self.artifacts_setup.timestamp}"
        logging.debug(f"MLFlow run name: {run_name}")
        return run_name

    def start_run(self, run_name: str):
        logging.info(f"Starting MLFlow run: {run_name}")
        return mlflow.start_run(run_name=run_name)

    def log_params(self, params: dict):
        try:
            logging.debug(f"Logging {len(params)} model parameters to MLFlow")
            result = mlflow.log_params(params)
            logging.debug("Model parameters logged successfully")
            return result
        except Exception as e:
            logging.error(f"Failed to log parameters to MLFlow: {e}")
            raise

    def log_artifacts(self, artifact_path):
        try:
            logging.debug(f"Logging evaluation plots from {artifact_path} to MLFlow")
            result = mlflow.log_artifacts(local_dir=artifact_path)
            logging.debug("Evaluation plots logged successfully")
            return result
        except Exception as e:
            logging.error(f"Failed to log artifacts to MLFlow: {e}")
            raise

    def log_metrics(self, metrics: dict):
        try:
            logging.debug(f"Logging {len(metrics)} evaluation metrics to MLFlow")
            result = mlflow.log_metrics(metrics)
            logging.debug("Evaluation metrics logged successfully")
            return result
        except Exception as e:
            logging.error(f"Failed to log metrics to MLFlow: {e}")
            raise      

    
    def log_model(self, model):
        try:
            logging.debug("Logging trained model to MLFlow")
            result = mlflow.xgboost.log_model(model, name="model")
            logging.debug("Trained model logged successfully")
            return result
        except Exception as e:
            logging.error(f"Failed to log model to MLFlow: {e}")
            raise      
        
