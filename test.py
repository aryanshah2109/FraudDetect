import os
import pandas as pd

from src.data.data_preprocessor import DataPreprocessor
from src.data.data_reader import DataLoader
from src.config import config_loader
from src.logger import logging

class TestPipeline:

    def __init__(self):
        config = config_loader.load_config()
        self.target_column_name = config["features"]["target_column_name"]
        self.random_state = config["seed"]
        self.test_size = config["training"]["test_size"]
        self.stratify = config["training"]["stratify"]

    def test_pipeline(self):

        try:
            logging.info("Initiating pipeline testing.")

            data = DataLoader().load_data()

            X_train, X_test, y_train, y_test = DataLoader().data_train_test_split(
                data,
                target_column_name = self.target_column_name,
                test_size = self.test_size,
                random_state = self.random_state,
                stratify = self.stratify
            )

            preprocessor = DataPreprocessor()

            X_train = preprocessor.fit_transform(X_train)
            X_test  = preprocessor.transform(X_test)

            preprocessor.save_preprocessed_data(
                X_train,
                X_test,
                y_train,
                y_test
            )
            logging.info("Successfully executed pipeline")

        except Exception as e:
            logging.error(f"Error while testing pipeline. {e}")
            raise

TestPipeline().test_pipeline()