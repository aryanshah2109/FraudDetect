import mlflow
from datetime import datetime

from src.config import config_loader
from src.logger import logging

from dotenv import load_dotenv
import os

load_dotenv()  

class MLFlowSetup:
    """
    Used to setup MLflow. Includes setting up tracking uri, experiment and runs
    """


    def __init__(self):
        config = config_loader.load_config()

        self.model_name = config["model"]["name"]

        self.tracking_uri = config["mlflow"]["mlflow_tracking_uri"]
        self.experiment_name = config["mlflow"]["experiment_name"]        

        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(self.experiment_name)

    def get_run_name(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.model_name}_{timestamp}"


    def start_run(self, run_name: str):
        logging.info("Starting run")
        return mlflow.start_run(run_name=run_name)

    def log_params(self, params: dict):
        try:
            logging.info("Logging parameters")
            return mlflow.log_params(params)
        except Exception as e:
            logging.error(f"Could not log parameters due to error: {e}")

    
    def log_artifacts(self, artifact_path):
        try:
            logging.info("Logging artifacts")
            return mlflow.log_artifacts(local_dir = artifact_path)
        except Exception as e:
            logging.error(f"Could not log artifacts due to error: {e}")
        

    def log_metrics(self, metrics: dict):
        try:
            logging.info("Logging metrics")
            return mlflow.log_metrics(metrics)
        except Exception as e:
            logging.error(f"Could not log metrics due to error: {e}")      

    
    def log_model(self, model):
        try:
            logging.info("Logging model")
            return mlflow.xgboost.log_model(model, name="model")
        except Exception as e:
            logging.error(f"Could not log model due to error: {e}")      
        
