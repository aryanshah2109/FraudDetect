import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, auc,
                             average_precision_score, confusion_matrix,
                             f1_score, precision_recall_curve, precision_score,
                             recall_score, roc_auc_score, roc_curve)

from src.config import config_loader
from src.logger import logging
from src.utils.artifacts_setup import ArtifactsSetup


class CalculateMetrics:
    def __init__(self, artifacts_setup: ArtifactsSetup):
        self.artifacts_setup = artifacts_setup
        self.artifacts_path = self.artifacts_setup.artifact_path
        self.artifacts_plots_path = self.artifacts_setup.artifacts_plots_path

        config = config_loader.load_config()
        self.precision_limit = config["metrics"]["precision_limit"]
    
    def calculate_thresholds(self, y_val: pd.Series, y_probabilities: pd.Series):
        try:
            logging.debug("Calculating optimal threshold using precision-recall curve")

            precisions, recalls, thresholds = precision_recall_curve(y_val, y_probabilities)

            # Remove last element (no threshold for last point)
            precisions = precisions[:-1]
            recalls = recalls[:-1]

            # Condition: Precision >= precision_limit
            valid_idx = np.where(precisions >= self.precision_limit)[0]

            if len(valid_idx) > 0:
                best_idx = valid_idx[np.argmax(recalls[valid_idx])]
                logging.debug(f"Threshold selected with precision >= {self.precision_limit}")
            else:
                # fallback to F1 if condition not met
                f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
                best_idx = np.argmax(f1_scores)
                logging.debug(f"No threshold meeting precision limit {self.precision_limit}, using F1 optimization")

            return thresholds[best_idx]

        except Exception as e:
            logging.error(f"Error while calculating threshold: {e}")
            raise


    def evaluate(self, y_test: pd.Series, y_pred: pd.Series, y_probabilities: pd.Series, threshold: float = None, dataset: str = "test"):
        try:
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_probabilities)
            pr_auc = average_precision_score(y_test, y_probabilities)
            cm = confusion_matrix(y_test, y_pred)            

            # Log metrics with dataset context
            logging.info(f"[{dataset.upper()}] Accuracy: {accuracy:.6f}")
            logging.info(f"[{dataset.upper()}] Precision: {precision:.6f}")
            logging.info(f"[{dataset.upper()}] Recall: {recall:.6f}")
            logging.info(f"[{dataset.upper()}] F1 Score: {f1:.6f}")
            logging.info(f"[{dataset.upper()}] ROC AUC: {roc_auc:.6f}")
            logging.info(f"[{dataset.upper()}] PR AUC: {pr_auc:.6f}")
            if threshold is not None:
                logging.info(f"[{dataset.upper()}] Threshold: {threshold:.6f}")
            logging.debug(f"[{dataset.upper()}] Confusion Matrix:\n{cm}")

            self.metrics = {
                "accuracy" : accuracy,
                "precision" : precision,
                "recall" : recall,
                "f1" : f1,
                "roc_auc" : roc_auc,
                "pr_auc" : pr_auc,
                "confusion_matrix" : cm.tolist()
            }
            
            if threshold is not None:
                self.metrics["threshold"] = threshold

            return self.metrics

        except Exception as e:
            logging.error(f"Error evaluating model on {dataset} set: {e}")
            raise

    def save_metrics_plots(self, y_test: pd.Series, y_pred: pd.Series, y_probabilities: pd.Series):
        try:
            logging.info("Saving metrics as artifact")
            self.artifacts_setup.save_json(self.metrics, "metrics.json")
            
            logging.debug("Saving confusion matrix plot")
            cm_path = self.artifacts_plots_path / "confusion_matrix.png"
            cm = confusion_matrix(y_test, y_pred)
            disp = ConfusionMatrixDisplay(cm)
            disp.plot(cmap="Blues", values_format="d")
            plt.savefig(cm_path)
            plt.close()

            logging.debug("Saving ROC-AUC curve plot")
            auc_path = self.artifacts_plots_path / "auc_curve.png"
            fpr, tpr, thresholds = roc_curve(y_test, y_probabilities)
            roc_auc = auc(fpr, tpr)
            plt.figure(figsize=(6,5))
            plt.plot(fpr, tpr, label=f"AUC: {roc_auc:.4f}")
            plt.plot([0,1], [0,1], linestyle="--", label="Random")
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title("ROC-AUC Curve")
            plt.legend(loc="lower right")
            plt.tight_layout()
            plt.savefig(auc_path)
            plt.close()

            logging.debug("Saving Precision-Recall curve plot")
            pr_auc_path = self.artifacts_plots_path / "pr_auc.png"
            precision, recall, thresholds = precision_recall_curve(y_test, y_probabilities)
            pr_auc = average_precision_score(y_test, y_probabilities)
            plt.figure(figsize=(6,5))
            plt.plot(recall, precision, label=f"AP: {pr_auc:.4f}")    
            baseline = sum(y_test) / len(y_test)
            plt.hlines(baseline, 0, 1, linestyles="--", label="Baseline")
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            plt.title("Precision-Recall Curve")
            plt.legend(loc="upper right")
            plt.tight_layout()
            plt.savefig(pr_auc_path)
            plt.close()
            
            logging.debug("Evaluation plots saved successfully")

        except Exception as e:
            logging.error(f"Could not save metrics as artifact: {e}")
            raise
