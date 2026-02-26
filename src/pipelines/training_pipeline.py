from src.config import config_loader
from src.data.data_reader import DataReader
from src.data.data_preprocessor import DataPreprocessor
from src.logger import logging

class TrainingPipeline:
    """
    The entire end-to-end training pipeline from data reading to model evaluation and inference
    """

    def __init__(self):
        self.config = config_loader.load_config()
        self.preprocesser = DataPreprocessor()

    def start_data_ingestion(self):
        """
        Phase 1 of training pipeline: Reads data from disk
        """

        data = DataReader().load_data()
        return data

    def split_data_into_train_test(self):
        """
        Phase 2 of training pipeline: Splits data into train and test sets
        """

        target_column_name = self.config["features"]["target_column_name"]
        random_state = self.config["seed"]
        test_size = self.config["training"]["test_size"]
        stratify = self.config["training"]["stratify"]

        

