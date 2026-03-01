import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split

from src.config import config_loader
from src.data.data_reader import DataReader
from src.data.data_preprocessor import DataPreprocessor
from src.training.model_training import ModelTrainer
from src.evaluation.metrics import CalculateMetrics
from src.logger import logging
from src.utils.mlflow_setup import MLFlowSetup
from src.utils.artifacts_setup import ArtifactsSetup

class TrainingPipeline:

    def __init__(self):
        self.config = config_loader.load_config()

        self.artifacts_setup = ArtifactsSetup()
        self.artifacts_path = self.artifacts_setup.artifact_path

        self.data_reader = DataReader(self.artifacts_setup)
        self.preprocessor = DataPreprocessor(self.artifacts_setup)
        self.model = ModelTrainer(self.artifacts_setup)
        self.metrics_object = CalculateMetrics(self.artifacts_setup)
        self.mlflow_object = MLFlowSetup(self.artifacts_setup)
    

    def split_data(self, data):
        logging.info("Splitting data into train and test")
        return self.data_reader.data_train_test_split(
            data=data,
            target_column_name=self.config["features"]["target_column_name"],
            test_size=self.config["training"]["test_size"],
            random_state=self.config["seed"],
            stratify=self.config["training"]["stratify"]
        )

    def split_train_validation(self, X_train, y_train):
        logging.info("Splitting train data into train and validation")
        return train_test_split(
            X_train,
            y_train,
            test_size=self.config["training"]["test_size"],
            random_state=self.config["seed"],
            stratify=y_train
        )

    def preprocess_data(self, X_train, X_val, X_test):
        logging.info("Preprocessing train, validation and test data")
        X_train_t = self.preprocessor.fit_transform(X_train)
        X_val_t = self.preprocessor.transform(X_val)
        X_test_t = self.preprocessor.transform(X_test)
        return X_train_t, X_val_t, X_test_t
    
    def train_model(self, X_train, y_train):
        logging.info("Training model")
        self.model.fit(X_train, y_train)

    def tune_threshold(self, y_val, y_val_prob):
        logging.info("Tuning threshold using validation data")
        return self.metrics_object.calculate_thresholds(y_val, y_val_prob)

    def evaluate_model(self, y_test, y_test_prob, threshold) -> dict:
        logging.info("Evaluating model on test data")
        y_pred = (y_test_prob >= threshold).astype(int)
        metrics = self.metrics_object.evaluate(y_test, y_pred, y_test_prob)
        metrics["threshold"] = float(threshold)
        self.metrics_object.save_metrics_plots(y_test, y_pred, y_test_prob)
        return metrics

    def run_pipeline(self):
        try:
            logging.info("Running training pipeline")

            data = self.data_reader.load_data()

            X_train, X_test, y_train, y_test = self.split_data(data)


            X_train, X_val, y_train, y_val = self.split_train_validation(X_train, y_train)

            X_train_t, X_val_t, X_test_t = self.preprocess_data(X_train, X_val, X_test)

            self.preprocessor.save_preprocessed_train_data(X_train_t, y_train)
            self.preprocessor.save_preprocessed_test_data(X_test_t, y_test)
            self.preprocessor.save_preprocessor_pipeline()

            self.train_model(X_train_t, y_train)

            y_val_prob = self.model.predict_probability(X_val_t)

            run_name = self.mlflow_object.get_run_name()

            with self.mlflow_object.start_run(run_name):                

                best_threshold = self.tune_threshold(y_val, y_val_prob)

                logging.info(f"Best threshold selected: {best_threshold}")

                y_test_prob = self.model.predict_probability(X_test_t)

                params = self.model.get_params()            

                self.model.save_model()
                self.model.save_params()

                metrics = self.evaluate_model(y_test, y_test_prob, best_threshold)

                clean_metrics = {}

                for k, v in metrics.items():
                    if isinstance(v, (int, float)):
                        clean_metrics[k] = float(v)
                
                self.mlflow_object.log_params({"decision_threshold": float(best_threshold)})
                self.mlflow_object.log_artifacts(self.artifacts_setup.artifacts_plots_path)
                self.mlflow_object.log_model(self.model.get_model())
                self.mlflow_object.log_params(params)
                self.mlflow_object.log_metrics(clean_metrics)

            logging.info("Pipeline completed successfully")

        except Exception as e:
            logging.error(f"Error occurred while running pipeline: {e}")
            raise