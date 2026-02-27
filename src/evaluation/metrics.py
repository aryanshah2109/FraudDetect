import pandas as pd
import numpy as np

from src.logger import logging
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    precision_recall_curve,
    average_precision_score
)


class CalculateMetrics:

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

        except Exception as e:
            logging.error(f"Error while evaluating model: {e}")
            raise