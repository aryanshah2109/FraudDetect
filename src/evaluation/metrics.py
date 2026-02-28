import pandas as pd
import numpy as np

from src.utils.artifacts_setup import ArtifactsSetup
from src.logger import logging
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    precision_recall_curve,
    average_precision_score,

)


class CalculateMetrics:
    def __init__(self):
        self.artifacts_object = ArtifactsSetup()
        self.artifacts_path = self.artifacts_object.get_artifact_dir_name()

    def calculate_thresholds(self, y_test: pd.Series, y_probabilities: pd.Series):
        try:
            logging.info("Calculating optimal threshold using precision-recall curve")

            precisions, recalls, thresholds = precision_recall_curve(y_test, y_probabilities)

            f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (
                precisions[:-1] + recalls[:-1] + 1e-8
            )

            best_idx = np.argmax(f1_scores)
            return thresholds[best_idx]

        except Exception as e:
            logging.error(f"Error while calculating thresholds: {e}")
            raise


    def evaluate(self, y_test: pd.Series, y_pred: pd.Series, y_probabilities: pd.Series):
        try:
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_probabilities)
            pr_auc = average_precision_score(y_test, y_probabilities)
            cm = confusion_matrix(y_test, y_pred)

            

            logging.info(f"Accuracy: {accuracy}")
            logging.info(f"Precision: {precision}")
            logging.info(f"Recall: {recall}")
            logging.info(f"F1 Score: {f1}")
            logging.info(f"ROC AUC: {roc_auc}")
            logging.info(f"PR AUC: {pr_auc}")
            logging.info(f"Confusion Matrix:\n{cm}")

            self.metrics = {
                "accuracy" : accuracy,
                "precision" : precision,
                "recall" : recall,
                "f1" : f1,
                "roc_auc" : roc_auc,
                "pr_auc" : pr_auc,
                "confusion_matrix" : cm.tolist()
            }

            return self.metrics

        except Exception as e:
            logging.error(f"Error while evaluating model: {e}")
            raise


    def save_metrics(self):
        try:
            logging.info("Saving metrics as artifact")
            self.artifacts_object.save_json(self.metrics, "metrics.json")
        
        except Exception as e:
            logging.error("Could not save metrics as artifact")