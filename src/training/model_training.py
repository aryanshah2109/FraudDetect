import pandas as pd
from xgboost import XGBClassifier

from src.config import config_loader
from src.logger import logging
from src.utils.artifacts_setup import ArtifactsSetup


class ModelTrainer:

    def __init__(self, artifacts_setup: ArtifactsSetup):
        config = config_loader.load_config()
        self.artifacts_setup = artifacts_setup
        self.artifacts_path = self.artifacts_setup.artifact_path

        self.n_estimators = config["model"]["parameters"]["n_estimators"]
        self.max_depth = config["model"]["parameters"]["max_depth"]
        self.learning_rate = config["model"]["parameters"]["learning_rate"]
        self.subsample = config["model"]["parameters"]["subsample"]
        self.colsample_bytree = config["model"]["parameters"]["colsample_bytree"]
        self.scale_pos_weight = config["model"]["parameters"]["scale_pos_weight"]
        self.random_state = config["seed"]
        self.objective = config["model"]["parameters"]["objective"]
        self.eval_metric = config["model"]["parameters"]["eval_metric"]
        self.tree_method = config["model"]["parameters"]["tree_method"]
        self.device = config["model"]["parameters"]["device"]
        self.predictor = config["model"]["parameters"]["predictor"]
        self.n_jobs = config["model"]["parameters"]["n_jobs"]
        


        self.model = XGBClassifier(
            n_estimators = self.n_estimators,
            max_depth = self.max_depth,
            learning_rate = self.learning_rate, 
            subsample = self.subsample,
            colsample_bytree = self.colsample_bytree,
            scale_pos_weight = self.scale_pos_weight,
            random_state = self.random_state,
            objective = self.objective,
            eval_metric = self.eval_metric,
            tree_method = self.tree_method,
            device = self.device,
            predictor = self.predictor,
            n_jobs = self.n_jobs
        )


    def fit(self, X_train: pd.DataFrame, y_train: pd.DataFrame):
        try:
            logging.info("Initiating training on given model")            

            self.model.fit(X_train, y_train)

            logging.info("Successful training on given model")            

        except Exception as e:
            logging.error(f"Error while training model: {e}")
            raise

    def predict(self, X_test: pd.DataFrame) -> pd.Series:
        """
        Predicts on test data and returns pandas Series object of prediction values
        """

        try:
            logging.info("Initiating testing on given test data")            

            y_pred = self.model.predict(X_test)

            logging.info("Successful testing on given test data")            

            return y_pred            

        except Exception as e:
            logging.error(f"Error while testing on test data: {e}")
            raise

    def predict_probability(self, X: pd.DataFrame, dataset: str = "test") -> pd.Series:
        """
        Computes prediction probabilities for the given dataset
        
        Args:
            X: Feature data
            dataset: Dataset identifier ('validation', 'test', etc.) for logging
        
        Returns:
            Probability predictions for positive class
        """
        try:
            logging.debug(f"Computing probability predictions for {dataset} set (shape: {X.shape})")
            y_probability = self.model.predict_proba(X)[:, 1]
            logging.debug(f"Probability predictions computed for {dataset} set")
            return y_probability            

        except Exception as e:
            logging.error(f"Error computing probability predictions for {dataset} set: {e}")
            raise

    def get_params(self):
        """
        Returns parameters of model used during training
        """

        try:
            logging.debug("Fetching parameters used during training")
            self.params = self.model.get_params()
            return self.params
        
        except Exception as e:
            logging.error(f"Could not fetch parameters: {e}")
            raise


    def get_model(self):
        """
        Returns model created during training
        """

        try:
            logging.debug("Fetching model created during training")
            return self.model
        
        except Exception as e:
            logging.error(f"Could not fetch model: {e}")
            raise

    def save_model(self):
        try:
            logging.debug("Saving trained model to artifacts")
            self.artifacts_setup.save_model(self.model, "xgboost_model.pkl")
            logging.debug("Model saved successfully")
        
        except Exception as e:
            logging.error(f"Failed to save model artifact: {e}")
            raise

    def save_params(self):
        try:
            logging.debug("Saving model parameters to artifacts")
            self.artifacts_setup.save_json(self.params, "params.json")
            logging.debug("Model parameters saved successfully")
        
        except Exception as e:
            logging.error(f"Failed to save model parameters: {e}")
            raise



