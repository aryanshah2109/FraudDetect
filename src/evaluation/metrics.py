import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.utils.artifacts_setup import ArtifactsSetup
from src.config import config_loader
from src.logger import logging
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    auc,
    confusion_matrix,
    precision_recall_curve,
    average_precision_score,
    ConfusionMatrixDisplay,
)


class CalculateMetrics:
    def __init__(self, artifacts_setup: ArtifactsSetup):
        self.artifacts_setup = artifacts_setup
        self.artifacts_path = self.artifacts_setup.artifact_path
        self.artifacts_plots_path = self.artifacts_setup.artifacts_plots_path

        config = config_loader.load_config()
        self.precision_limit = config["metrics"]["precision_limit"]
    
    def calculate_thresholds(self, y_test: pd.Series, y_probabilities: pd.Series):
        try:
            logging.info("Calculating optimal threshold using precision-recall curve")

            precisions, recalls, thresholds = precision_recall_curve(y_test, y_probabilities)

            # Remove last element (no threshold for last point)
            precisions = precisions[:-1]
            recalls = recalls[:-1]

            # Condition: Precision >= precision_limit
            valid_idx = np.where(precisions >= self.precision_limit)[0]

            if len(valid_idx) > 0:
                best_idx = valid_idx[np.argmax(recalls[valid_idx])]
            else:
                # fallback to F1 if condition not met
                f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
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

    def save_plots(self, y_test: pd.Series, y_pred: pd.Series, y_probabilities: pd.Series):
        try:
            logging.info("Saving confusion metrics as artifact")
            cm_path = self.artifacts_plots_path / "confusion_matrix.png"
            confusion_matrix_artifact = confusion_matrix(y_test, y_pred)
            disp = ConfusionMatrixDisplay(confusion_matrix_artifact)
            disp.plot(cmap="Blues", values_format="d")
            plt.savefig(cm_path)
            plt.close()

            logging.info("Saving AUC curve as artifact")
            auc_path = self.artifacts_plots_path / "auc_curve.png"
            fpr, tpr, thresholds = roc_curve(y_test, y_probabilities)
            roc_auc = auc(fpr, tpr)
            plt.figure(figsize=(6,5))
            plt.plot(fpr, tpr, label=f"AUC:{roc_auc:.4f}")
            plt.plot([0,1], [0,1], linestyle="--")
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.legend(loc="lower right")
            plt.tight_layout()
            plt.savefig(auc_path)
            plt.close()

            logging.info("Saving PR-AUC as artifact")
            pr_auc_path = self.artifacts_plots_path / "pr_auc.png"
            precision, recall, thresholds = precision_recall_curve(y_test, y_probabilities)
            pr_auc = average_precision_score(y_test, y_probabilities)
            plt.figure(figsize=(6,5))
            plt.plot(recall, precision, label=f"AP = {pr_auc:.4f}")    
            # baseline = proportion of positive class
            baseline = sum(y_test) / len(y_test)
            plt.hlines(baseline, 0, 1, linestyles="--")
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            plt.title("Precision-Recall Curve")
            plt.legend(loc="upper right")
            plt.tight_layout()
            plt.savefig(pr_auc_path)
            plt.close()         


        except Exception as e:
            logging.error(f"Could not save plots due to error: {e}")




    def save_metrics_plots(self, y_test: pd.Series, y_pred: pd.Series, y_probabilities: pd.Series):
        try:
            logging.info("Saving metrics as artifact")
            self.artifacts_setup.save_json(self.metrics, "metrics.json")
            self.save_plots(y_test, y_pred, y_probabilities)
        
        except Exception as e:
            logging.error("Could not save metrics as artifact")
