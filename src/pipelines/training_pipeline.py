import pandas as pd
import numpy as np
import joblib
import time

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
        logging.debug(f"Training data transformed: {X_train_t.shape}")
        
        X_val_t = self.preprocessor.transform(X_val)
        logging.debug(f"Validation data transformed: {X_val_t.shape}")
        
        X_test_t = self.preprocessor.transform(X_test)
        logging.debug(f"Test data transformed: {X_test_t.shape}")
        
        return X_train_t, X_val_t, X_test_t
    
    def train_model(self, X_train, y_train):
        start_time = time.time()
        logging.info("Training model started")
        self.model.fit(X_train, y_train)
        elapsed_time = time.time() - start_time
        logging.info(f"Model training completed in {elapsed_time:.2f} seconds")

    def tune_threshold(self, y_val, y_val_prob):
        logging.info("Threshold tuning: calculating optimal threshold from validation set")
        threshold = self.metrics_object.calculate_thresholds(y_val, y_val_prob)
        logging.info(f"Threshold selected from validation set: {threshold:.6f}")
        
        # Compute validation metrics for selected threshold
        y_val_pred = (y_val_prob >= threshold).astype(int)
        val_metrics = self.metrics_object.evaluate(y_val, y_val_pred, y_val_prob, dataset="validation")
        
        return threshold

    def evaluate_model(self, y_test, y_test_prob, threshold) -> dict:
        start_time = time.time()
        logging.info("Evaluating model on test set")
        y_pred = (y_test_prob >= threshold).astype(int)
        metrics = self.metrics_object.evaluate(y_test, y_pred, y_test_prob, dataset="test")
        logging.debug("Generating evaluation plots")
        self.metrics_object.save_metrics_plots(y_test, y_pred, y_test_prob)
        elapsed_time = time.time() - start_time
        logging.debug(f"Model evaluation completed in {elapsed_time:.2f} seconds")
        return metrics

    def run_pipeline(self):
        try:
            pipeline_start_time = time.time()
            logging.info("TRAINING PIPELINE STARTED")

            # Data Loading
            logging.info("\n[STAGE 1] Data Loading")
            data = self.data_reader.load_data()
            logging.debug(f"Raw data shape: {data.shape}")

            # Data Splitting
            logging.info("\n[STAGE 2] Data Splitting")
            X_train, X_test, y_train, y_test = self.split_data(data)
            logging.debug(f"Train set: {X_train.shape}, Test set: {X_test.shape}")

            X_train, X_val, y_train, y_val = self.split_train_validation(X_train, y_train)
            logging.debug(f"Train set: {X_train.shape}, Validation set: {X_val.shape}, Test set: {X_test.shape}")

            # Data Preprocessing
            logging.info("\n[STAGE 3] Data Preprocessing")
            X_train_t, X_val_t, X_test_t = self.preprocess_data(X_train, X_val, X_test)
            
            logging.debug("Saving preprocessed datasets and preprocessing pipeline")
            self.preprocessor.save_preprocessed_train_data(X_train_t, y_train)
            self.preprocessor.save_preprocessed_test_data(X_test_t, y_test)
            self.preprocessor.save_preprocessor_pipeline()

            # Model Training
            logging.info("\n[STAGE 4] Model Training")
            self.train_model(X_train_t, y_train)

            # Validation: Predict probabilities for threshold tuning
            logging.info("\n[STAGE 5] Validation & Threshold Tuning")
            logging.debug("Computing validation predictions for threshold selection")
            y_val_prob = self.model.predict_probability(X_val_t, dataset="validation")

            run_name = self.mlflow_object.get_run_name()

            with self.mlflow_object.start_run(run_name):
                # Threshold tuning on validation set
                best_threshold = self.tune_threshold(y_val, y_val_prob)

                # Test: Predict probabilities (only once)
                logging.info("\n[STAGE 6] Model Evaluation on Test Set")
                logging.debug("Computing test predictions")
                y_test_prob = self.model.predict_probability(X_test_t, dataset="test")

                # Get model parameters once
                logging.debug("Extracting model parameters")
                params = self.model.get_params()

                # Save model and parameters
                logging.info("Saving model and parameters as artifacts")
                self.model.save_model()
                self.model.save_params()

                # Evaluate on test set
                metrics = self.evaluate_model(y_test, y_test_prob, best_threshold)

                # Clean metrics for MLflow (remove non-numeric types)
                clean_metrics = {}
                for k, v in metrics.items():
                    if isinstance(v, (int, float)):
                        clean_metrics[k] = float(v)

                # Log to MLflow in correct order: params -> metrics -> artifacts -> model
                logging.info("\n[STAGE 7] MLFlow Logging")
                logging.debug("Logging model parameters to MLFlow")
                self.mlflow_object.log_params(params)
                
                logging.debug("Logging evaluation metrics to MLFlow")
                self.mlflow_object.log_metrics(clean_metrics)
                
                logging.debug("Logging evaluation plots to MLFlow")
                self.mlflow_object.log_artifacts(self.artifacts_setup.artifacts_plots_path)
                
                self.mlflow_object.log_model(self.model.get_model())

            # Final Summary
            pipeline_elapsed_time = time.time() - pipeline_start_time
            logging.info("PIPELINE SUMMARY")
            logging.info(f"Threshold: {best_threshold:.6f}")
            logging.info(f"Precision: {clean_metrics.get('precision', 'N/A'):.4f}")
            logging.info(f"Recall: {clean_metrics.get('recall', 'N/A'):.4f}")
            logging.info(f"F1 Score: {clean_metrics.get('f1', 'N/A'):.4f}")
            logging.info(f"ROC AUC: {clean_metrics.get('roc_auc', 'N/A'):.4f}")
            logging.info(f"PR AUC: {clean_metrics.get('pr_auc', 'N/A'):.4f}")
            logging.info(f"Total Pipeline Time: {pipeline_elapsed_time:.2f} seconds")
            logging.info("TRAINING PIPELINE COMPLETED SUCCESSFULLY")

        except Exception as e:
            logging.error(f"Pipeline execution failed: {e}", exc_info=True)
            raise