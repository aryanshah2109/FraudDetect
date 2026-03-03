import os
import pandas as pd

from src.config import config_loader
from src.logger import logging
from src.pipelines.feature_engineering_pipeline import BalanceErrorFeatureGenerator

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class DataPreprocessingPipelineGenerator:
    """
    Class to generate a pipeline for data preprocessing
    """

    def __init__(self):
        config = config_loader.load_config()
        self.numerical_columns = config["features"]["num_cols"]
        self.categorical_columns = config["features"]["cat_cols"]
    
    def generate_categorical_pipeline(self):
        """
            Function that generatees a data preprocessing pipeline for categorical columns and returns the pipeline
        """
        try:
            logging.debug("Generating categorical column preprocessing pipeline")

            categorical_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore"))
            ])        

            return categorical_pipeline
        
        except Exception as e:
            logging.error(f"Could not generate categorical pipeline due to error: {e}")
            raise

    def generate_numerical_pipeline(self):
        """
            Function that generatees a data preprocessing pipeline for numerical columns and returns the pipeline
        """
        try:
            logging.debug("Generating numerical column preprocessing pipeline")

            numerical_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])        

            return numerical_pipeline
        
        except Exception as e:
            logging.error(f"Could not generate numerical pipeline due to error: {e}")
            raise


    def generate_pipeline(self):
        """
            Function that generatees a data preprocessing pipeline and returns the pipeline
        """

        try:

            logging.info("Generating preprocessing column transformer")

            numerical_pipeline = self.generate_numerical_pipeline()
            categorical_pipeline = self.generate_categorical_pipeline()

            preprocessor = ColumnTransformer(transformers = [
                ("numerical", numerical_pipeline, self.numerical_columns),
                ("categorical", categorical_pipeline, self.categorical_columns)
            ], remainder="drop")
            
            full_pipeline = Pipeline(steps=[
                ("feature_engineering", BalanceErrorFeatureGenerator()),
                ("column_transform", preprocessor)
            ])

            return full_pipeline
        
        except Exception as e:
            logging.error(f"Could not generate column transformer due to error: {e}")
            raise