import os
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.path_constants import (INTERIM_TEST_DATA_PATH,
                                INTERIM_TRAIN_DATA_PATH, RAW_DATA_PATH)
from src.utils.artifacts_setup import ArtifactsSetup


class DataReader:
    """
    Data loader loads data file from disk and also performs train test split if needed
    """

    def __init__(self, artifacts_object: ArtifactsSetup):
        self.data_path = RAW_DATA_PATH
        self.interim_train_path = INTERIM_TRAIN_DATA_PATH
        self.interim_test_path = INTERIM_TEST_DATA_PATH
        self.artifacts_setup = artifacts_object
        self.artifacts_path = self.artifacts_setup.artifact_path

        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data not found at path {RAW_DATA_PATH}")

    
    def load_data(self) -> pd.DataFrame:
        """
            Reads data from disk and returns the Pandas DataFrame object of the data file
        """

        try:
            
            logging.info("Initiating data reading from disk...")

            data = pd.read_csv(self.data_path)

            logging.info(f"Successfully read data. Shape: {data.shape}")

            return data
        
        except Exception as e:
            logging.error(f"Could not load data due to error: {e}")
            raise

    def save_train_test_data(self, X_train:pd.DataFrame, X_test:pd.DataFrame, y_train:pd.Series, y_test:pd.Series):
        """
        Takes train and test splits of data and saves the csv files in specific path
        """

        try:
            logging.info("Save train and test interim data folder and artifacts")

            train_raw = pd.concat([X_train, y_train], axis=1)   # Merge X and y train data into single train file
            test_raw = pd.concat([X_test, y_test], axis=1)    # Merge X and y test data into single test file

            train_raw.to_csv(self.interim_train_path)
            test_raw.to_csv(self.interim_test_path)
            
            self.artifacts_setup.save_csv_artifact(train_raw, "train_raw")
            self.artifacts_setup.save_csv_artifact(test_raw, "test_raw")
            
        except Exception as e:
            logging.error(f"Could not save train test interim data to interim folder and artifacts due to error {e}")
            raise

        return 

    def data_train_test_split(
            self,
            data: pd.DataFrame,
            target_column_name: str,
            test_size: float = 0.2,
            random_state: int = 42,
            stratify: bool = True
        ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
            Performs train and test splits of data file and returns train and test splits of 
            data seperated into features and target
        """

        try:

            logging.info("Initiating train test split of data...")

            logging.debug("Assigning features and target from data")
            X = data.drop(columns = target_column_name)
            y = data[target_column_name]

            logging.debug("Stratifying target column if needed to maintain class proportion")
            stratify_column = y if stratify else None

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size = test_size,
                random_state = random_state,
                stratify = stratify_column      
                # stratify used to equally divide all classes of target column among train and test data
            )

            logging.info("Successfully split data into train and test data")
            
            self.save_train_test_data(X_train, X_test, y_train, y_test)

            return (X_train, X_test, y_train, y_test)
        
        except Exception as e:
            logging.error(f"Could not perform train test split due to error : {e}")
            raise  