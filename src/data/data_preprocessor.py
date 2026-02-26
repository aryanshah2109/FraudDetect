import pandas as pd

from src.logger import logging
from src.path_constants import PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH
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

    
    
    def save_preprocessed_train_data(self, X_train:pd.DataFrame, y_train:pd.Series):
        """
        Method to save preprocessed train data
        """
        try:

            logging.info("Saving preprocessed train data to csv file")

            train_data = pd.concat([X_train, y_train])
            
            train_data.to_csv(PROCESSED_TRAIN_DATA_PATH)

            logging.info("Successfully saved preprocessed train data to csv file")
        
        except Exception as e:
            logging.error(f"Error while saving preprocesed train data: {e}")
            raise

    def save_preprocessed_test_data(self, X_test:pd.DataFrame, y_test:pd.Series):
        """
        Method to save preprocessed train data
        """
        try:

            logging.info("Saving preprocessed test data to csv file")

            test_data = pd.concat([X_test, y_test])
            
            test_data.to_csv(PROCESSED_TEST_DATA_PATH)

            logging.info("Successfully saved preprocessed test data to csv file")
        
        except Exception as e:
            logging.error(f"Error while saving preprocesed test data: {e}")
            raise

    