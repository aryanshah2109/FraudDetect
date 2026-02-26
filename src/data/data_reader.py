import os
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.path_constants import RAW_DATA_PATH


class DataLoader:
    """
    Data loader loads data file from disk and also performs train test split if needed
    """

    def __init__(self):
        self.data_path = RAW_DATA_PATH

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

            logging.debug("Stratifing target column if needed to maintain class proportion")
            stratify_column = y if stratify else None

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size = test_size,
                random_state = random_state,
                stratify = stratify_column
            )

            logging.info("Successfully split data into train and test data")

            return (X_train, X_test, y_train, y_test)
        
        except Exception as e:
            logging.error(f"Could not perform train test split due to error : {e}")
            raise  