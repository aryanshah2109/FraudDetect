import os

import pandas as pd

from src.logger import logging
from src.path_constants import PROCESSED_DATA_PATH
from src.config import config_loader

from src.pipelines.data_preprocessing_pipeline_generator import DataPreprocessingPipelineGenerator


class DataPreprocessor:
    """
    Preprocesses data and transform into trainable data.
    """

    def __init__(self):
        
        self.preprocessing_pipeline = DataPreprocessingPipelineGenerator().generate_pipeline()
        
        config = config_loader.load_config()
        self.numerical_columns = config["features"]["num_cols"]
        self.categorical_columns = config["features"]["cat_cols"]

    def fit_transform(self, X: pd.DataFrame):
        """
        Encodes categorical values and scales numerical values via pipeline during training
        """
        try:
            logging.info("Encoding categorical values and scaling numerical columns")
            X_transformed = self.preprocessing_pipeline.fit_transform(X)
            X_column_names = self.preprocessing_pipeline.get_feature_names_out()

            # Convert back to dataframe
            X_transformed_df = pd.DataFrame(
                X_transformed, 
                columns = X_column_names,
                index = X.index
            )

            return X_transformed_df
        
        except Exception as e:
            logging.error(f"Error while handling categorical and numerical values: {e}")
            raise

    def transform(self, X: pd.DataFrame):
        """
        Encodes categorical values and scales numerical values via pipeline during inference
        """
        try:
            logging.info("Encoding categorical values and scaling numerical columns")
            X_transformed = self.preprocessing_pipeline.transform(X)
            X_column_names = self.preprocessing_pipeline.get_feature_names_out()

            # Convert back to dataframe
            X_transformed_df = pd.DataFrame(
                X_transformed, 
                columns = X_column_names,
                index = X.index
            )

            return X_transformed_df
        
        except Exception as e:
            logging.error(f"Error while handling categorical and numerical values: {e}")
            raise

    def preprocess_train_data(self, X: pd.DataFrame):
        """
        Main method that merges all preprocessing functions
        """
        try:
            logging.info("Performing preprocessing on features")

            X_processed = self.fit_transform(X)

            return X_processed
        
        except Exception as e:
            logging.error(f"Error while preprocessing features: {e}")
            raise
    
    def preprocess_test_data(self, X: pd.DataFrame):
        """
        Main method that merges all preprocessing functions
        """
        try:
            logging.info("Performing preprocessing on features")

            X_processed = self.transform(X)

            return X_processed
        
        except Exception as e:
            logging.error(f"Error while preprocessing features: {e}")
            raise


    def save_preprocessed_data(self, X_train:pd.DataFrame, X_test:pd.DataFrame, y_train:pd.Series, y_test:pd.Series):
        """
        Method to save preprocessed features into data folder
        """
        try:

            logging.info("Saving preprocessed data to csv file")

            train_data = pd.concat([X_train, y_train])
            test_data = pd.concat([X_test, y_test])
            full_data = pd.concat([train_data, test_data], axis=0)
            full_data = full_data.reset_index(drop=True)
            full_data.to_csv(PROCESSED_DATA_PATH)

            logging.info("Successfully saved preprocessed data to csv file")
        
        except Exception as e:
            logging.error(f"Error while saving preprocesed data: {e}")
            raise

    