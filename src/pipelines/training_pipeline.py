import json
import time

import numpy as np
from sklearn.model_selection import train_test_split

from src.config import config_loader
from src.data.data_preprocessor import DataPreprocessor
from src.data.data_reader import DataReader
from src.evaluation.metrics import CalculateMetrics
from src.logger import logging
from src.model.model_picker import ModelPicker
from src.training.model_training import ModelTrainer
from src.utils.artifacts_setup import ArtifactsSetup
from src.utils.mlflow_setup import MLFlowSetup


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

        metric = self.config["metrics"]["model_picker_metric"]
        self.model_picker_object = ModelPicker(self.artifacts_setup, metric)

        self.schema_version = self.config["schema"]["version"]

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

        y_val_pred = (y_val_prob >= threshold).astype(int)
        self.metrics_object.evaluate(
            y_val,
            y_val_pred,
            y_val_prob,
            dataset="validation"
        )

        return threshold

    def evaluate_model(self, y_test, y_test_prob, threshold):
        start_time = time.time()
        logging.info("Evaluating model on test set")

        y_pred = (y_test_prob >= threshold).astype(int)

        metrics = self.metrics_object.evaluate(
            y_test,
            y_pred,
            y_test_prob,
            threshold=threshold,
            dataset="test"
        )

        self.metrics_object.save_metrics_plots(y_test, y_pred, y_test_prob)

        elapsed_time = time.time() - start_time
        logging.debug(f"Model evaluation completed in {elapsed_time:.2f} seconds")

        return metrics

    def run_pipeline(self):
        try:
            pipeline_start_time = time.time()
            logging.info("TRAINING PIPELINE STARTED")

            # STAGE 1: Data Loading
            logging.info("\n[STAGE 1] Data Loading")
            data = self.data_reader.load_data()
            logging.debug(f"Raw data shape: {data.shape}")

            # STAGE 2: Data Splitting
            logging.info("\n[STAGE 2] Data Splitting")
            X_train, X_test, y_train, y_test = self.split_data(data)

            X_train, X_val, y_train, y_val = self.split_train_validation(
                X_train, y_train
            )

            # STAGE 3: Data Preprocessing
            logging.info("\n[STAGE 3] Data Preprocessing")
            X_train_t, X_val_t, X_test_t = self.preprocess_data(
                X_train, X_val, X_test
            )

            self.preprocessor.save_preprocessed_train_data(X_train_t, y_train)
            self.preprocessor.save_preprocessed_test_data(X_test_t, y_test)
            self.preprocessor.save_preprocessor_pipeline()

            # STAGE 4: Model Training
            logging.info("\n[STAGE 4] Model Training")
            self.train_model(X_train_t, y_train)

            # STAGE 5: Validation & Threshold Tuning
            logging.info("\n[STAGE 5] Validation & Threshold Tuning")
            y_val_prob = self.model.predict_probability(
                X_val_t,
                dataset="validation"
            )

            run_name = self.mlflow_object.get_run_name()

            with self.mlflow_object.start_run(run_name):

                best_threshold = self.tune_threshold(y_val, y_val_prob)

                # STAGE 6: Test Evaluation
                logging.info("\n[STAGE 6] Model Evaluation on Test Set")
                y_test_prob = self.model.predict_probability(
                    X_test_t,
                    dataset="test"
                )

                params = self.model.get_params()

                self.model.save_model()
                self.model.save_params()

                metrics = self.evaluate_model(
                    y_test,
                    y_test_prob,
                    best_threshold
                )

                # Inject schema version
                metrics["schema_version"] = self.schema_version

                # Convert numpy types to native python types
                serializable_metrics = {}
                for k, v in metrics.items():
                    if isinstance(v, (np.floating, np.integer)):
                        serializable_metrics[k] = v.item()
                    else:
                        serializable_metrics[k] = v

                # Overwrite metrics.json in current run folder
                metrics_path = self.artifacts_setup.artifact_path / "metrics.json"
                with open(metrics_path, "w") as f:
                    json.dump(serializable_metrics, f, indent=4)

                # Prepare clean metrics for MLflow
                clean_metrics = {
                    k: float(v)
                    for k, v in serializable_metrics.items()
                    if isinstance(v, (int, float))
                }

                # MLflow logging
                logging.info("\n[STAGE 7] MLFlow Logging")
                self.mlflow_object.log_params(params)
                self.mlflow_object.log_metrics(clean_metrics)
                self.mlflow_object.log_artifacts(
                    self.artifacts_setup.artifacts_plots_path
                )
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

            # STAGE 8: Model Picking
            logging.info("\n[STAGE 8] Picking Best Model")
            self.model_picker_object.pick_best_model()

            logging.info(f"Total Pipeline Time: {pipeline_elapsed_time:.2f} seconds")
            logging.info("TRAINING PIPELINE COMPLETED SUCCESSFULLY")

        except Exception as e:
            logging.error(f"Pipeline execution failed: {e}", exc_info=True)
            raise