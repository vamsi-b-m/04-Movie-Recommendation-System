import os, sys
import pandas as pd

from src.utils import load_data

from src.entity.config_entity import DataManipulationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataManipulationArtifact



class FeatureGenerator:
    
    def __init__(self) -> None:
        pass
    
    def fit(self):
        pass

    def transform(self):
        pass

    def fit_transform(self):
        pass


class DataManipulation:
    
    def __init__(self, data_manipulation_config: DataManipulationConfig, data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            self.data_manipulation_config = data_manipulation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise Exception(e, sys) from e
        
    def read_data(self):
        try:
            ingested_train_file_path = self.data_ingestion_artifact.train_file_path
            ingested_test_file_path = self.data_ingestion_artifact.test_file_path
            
            train_dataset = load_data(file_path=ingested_train_file_path)
            test_dataset = load_data(file_path=ingested_test_file_path)

            return train_dataset, test_dataset
        except Exception as e:
            raise Exception(e, sys) from e
        
    def process_data(self):
        try:
            train_dataset, test_dataset = self.read_data()


        except Exception as e:
            raise Exception(e, sys) from e

    def initiate_data_manipulation(self):
        try:
            pass
        except Exception as e:
            raise Exception(e, sys) from e