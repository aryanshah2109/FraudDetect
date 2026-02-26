import pandas as pd

from src.config import config_loader
from src.data.data_reader import DataReader
from src.data.data_preprocessor import DataPreprocessor
from src.training.model_training import ModelTrainer
from src.logger import logging

class TrainingPipeline:
    """
    The entire end-to-end training pipeline from data reading to model evaluation and inference
    """

    def __init__(self):
        self.config = config_loader.load_config()
        self.preprocesser = DataPreprocessor()
        self.model = ModelTrainer()

    def start_data_ingestion(self):
        """
        Phase 1 of training pipeline: Reads data from disk
        """

        data = DataReader().load_data()
        return data

    def split_data_into_train_test(self, data: pd.DataFrame):
        """
        Phase 2 of training pipeline: Splits data into train and test sets
        """

        try:

            target_column_name = self.config["features"]["target_column_name"]
            random_state = self.config["seed"]
            test_size = self.config["training"]["test_size"]
            stratify = self.config["training"]["stratify"]

            X_train, X_test, y_train, y_test = DataReader().data_train_test_split(
                data = data,
                target_column_name = target_column_name,
                test_size = test_size,
                random_state = random_state,    
                stratify = stratify
            )        

            DataReader().save_train_test_data(X_train, X_test, y_train, y_test)

            return X_train, X_test, y_train, y_test

            
        
        except Exception as e:
            logging.log(f"Error while splitting data into train and test set: {e}")
            raise

    def preprocessing_train_data(self, X_train: pd.DataFrame, X_test: pd.DataFrame):

        try:
            X_train_transformed = self.preprocesser.fit_transform(X_train)
            X_test_transformed = self.preprocesser.transform(X_test)

            return X_train_transformed, X_test_transformed         
        
        except Exception as e:
            logging.error(f"Error while preprocessing data: {e}")
            raise
        
    def train_model(self, X_train: pd.DataFrame, y_train: pd.DataFrame):

        try:
            self.model.fit(X_train, y_train)
                   
        
        except Exception as e:
            logging.error(f"Error while training model: {e}")
            raise
        
    def test_model(self, X_test: pd.DataFrame):

        try:
            y_pred = self.model.predict(X_test)
            return y_pred
                   
        
        except Exception as e:
            logging.error(f"Error while predicting on test data: {e}")
            raise


    def run_pipeline(self):

        try:
            logging.info("Running pipeline.")

            logging.debug("Data Ingestion")
            data = self.start_data_ingestion()
            
            logging.debug("Train Test Split")
            X_train, X_test, y_train, y_test = self.split_data_into_train_test(data)
            
            logging.debug("Data Preprocessing")
            X_train_transformed, X_test_transformed = self.preprocessing_train_data(X_train, X_test)

            logging.debug("Save final train and test data")    
            self.preprocesser.save_preprocessed_train_data(X_train_transformed, y_train)
            self.preprocesser.save_preprocessed_test_data(X_test_transformed, y_test)

            logging.debug("Model Training")
            self.train_model(X_train_transformed, y_train)

            logging.debug("Model Testing on Test Data")
            y_pred = self.test_model(X_test)

            logging.debug("Evaluation Metrics")
            
        
        except Exception as e:
            logging.error(f"Error occured while running pipeline: {e}")
            raise





            


