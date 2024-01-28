import os, sys
from src.configuration.configuration import Configuration
from src.component.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact

class Pipeline:
    
    def __init__(self, config : Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise Exception(e, sys) from e