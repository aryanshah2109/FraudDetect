import pandas as pd
import joblib
from src.logger import logging
from src.path_constants import PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH
from src.config import config_loader
from src.pipelines.data_preprocessing_pipeline_generator import DataPreprocessingPipelineGenerator
from src.utils.artifacts_setup import ArtifactsSetup

class DataPreprocessor:

    def __init__(self):
        self.preprocessing_pipeline = DataPreprocessingPipelineGenerator().generate_pipeline()
        config = config_loader.load_config()
        self.numerical_columns = config["features"]["num_cols"]
        self.categorical_columns = config["features"]["cat_cols"]
        self.artifacts_object = ArtifactsSetup()
        self.artifacts_path = self.artifacts_object.get_artifact_dir_name()

    def fit_transform(self, X: pd.DataFrame):
        try:
            logging.info("Fitting and transforming training data")
            X_transformed = self.preprocessing_pipeline.fit_transform(X)
            X_column_names = self.preprocessing_pipeline.get_feature_names_out()

            df =  pd.DataFrame(
                X_transformed,
                columns=X_column_names,
                index=X.index
            )

            return df.astype(float)
        except Exception as e:
            logging.error(f"Error during fit_transform: {e}")
            raise

    def transform(self, X: pd.DataFrame):
        try:
            logging.info("Transforming data")
            X_transformed = self.preprocessing_pipeline.transform(X)
            X_column_names = self.preprocessing_pipeline.get_feature_names_out()

            df =  pd.DataFrame(
                X_transformed,
                columns=X_column_names,
                index=X.index
            )

            return df.astype(float)
        except Exception as e:
            logging.error(f"Error during transform: {e}")
            raise

    def save_preprocessed_train_data(self, X_train: pd.DataFrame, y_train: pd.Series):
        try:
            logging.info("Saving preprocessed train data")
            train_data = pd.concat([X_train, y_train], axis=1)
            train_data.to_csv(PROCESSED_TRAIN_DATA_PATH, index=False)
        except Exception as e:
            logging.error(f"Error saving preprocessed train data: {e}")
            raise

    def save_preprocessed_test_data(self, X_test: pd.DataFrame, y_test: pd.Series):
        try:
            logging.info("Saving preprocessed test data")
            test_data = pd.concat([X_test, y_test], axis=1)
            test_data.to_csv(PROCESSED_TEST_DATA_PATH, index=False)
        except Exception as e:
            logging.error(f"Error saving preprocessed test data: {e}")
            raise

    def save_preprocessor_pipeline(self):
        try:
            logging.info("Saving preprocessor pipeline as artifact")
            self.artifacts_object.save_pipeline(self.preprocessing_pipeline, "preprocessor.pkl")
        
        except Exception as e:
            logging.error("Could not save preprocessor pipeline as artifact")