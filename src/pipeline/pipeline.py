import os, sys
from src.configuration.configuration import Configuration
from src.component.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataCleaningArtifact
from src.entity.config_entity import DataCleaningConfig
from src.component.data_validation import DataValidation
from src.component.data_cleaning import DataCleaning

class Pipeline:
    
    def __init__(self, config : Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(config=self.config.get_data_ingestion_config())
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise Exception(e, sys) from e

    def start_data_cleaning(self, 
                            data_ingestion_artifact=DataIngestionArtifact,
                            data_cleaning_artifact=DataCleaningArtifact):
        try:
            data_cleaning = DataCleaning(data_cleaning_config=self.config.get_data_cleaning_config(),
                                         data_ingestion_artifact=data_ingestion_artifact)
            data_cleaning_artifact = data_cleaning.initiate_data_cleaning()
            return data_cleaning_artifact
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) \
            -> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact
                                             )
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise Exception(e, sys) from e
        
    def run_pipeline(self):
        data_ingestion_artifact = self.start_data_ingestion()
        data_cleaning_artifact = self.start_data_cleaning(data_ingestion_artifact=data_ingestion_artifact)
        #data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)