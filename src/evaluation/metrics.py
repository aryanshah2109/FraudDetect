import pandas as pd
import os

from src.config import config_loader
from src.logger import logging

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    auc,
    roc_curve,
    roc_auc_score,
    confusion_matrix,
    precision_recall_curve,
    ConfusionMatrixDisplay   
)

class CalculateMetrics:

    def __init__(self):
        pass

    def evaluate(self, y_test: pd.Series, y_pred: pd.Series):

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        confusion_matrix_evaluation = confusion_matrix(y_test, y_pred)
        auc_value = auc(y_test, y_pred)
        roc_auc_score_evaluation = roc_auc_score(y_test, y_pred)
        accuracy = (y_test, y_pred)