import os, sys
import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from kaggle.api.kaggle_api_extended import KaggleApi


class DataIngestion:
    
    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'='*20}Data Ingestion log Started.{'='*20}\n\n")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Exception(e, sys) from e
        
    def download_dataset_zip_file(self):
        try:
            self.data_ingestion_config
            api = KaggleApi()
            api.authenticate()
            dataset_url = self.data_ingestion_config.kaggle_dataset_url
            zip_data_dir = self.data_ingestion_config.zip_data_dir
            # raw_data_dir = self.data_ingestion_config.raw_data_dir
            # processed_data_dir = self.data_ingestion_config.processed_data_dir
            # processed_train_data_dir = self.data_ingestion_config.processed_train_data_dir
            # processed_test_data_dir = self.data_ingestion_config.processed_test_data_dir

            if os.path.exists(zip_data_dir):
                os.remove(zip_data_dir)

            os.makedirs(zip_data_dir, exist_ok=True)

            api.dataset_download_files(dataset=dataset_url, path=zip_data_dir, unzip=False)
            # dataset_url = data_ingestion_config_info[DATA_INGESTION_KAGGLE_DATASET_URL_KEY]
            # download_path = os.path.join(self.config_info[DATA_DIR_KEY], data_ingestion_config_info[DATA_INGESTION_ZIP_DATA_DIR_KEY])
            # os.makedirs(download_path, exist_ok=True)
            # api.dataset_download_files(dataset=dataset_url, path=download_path, unzip=False)
            
            return zip_data_dir
        except Exception as e:
            raise Exception(e, sys)

    def extract_dataset(self):
        pass

    def data_splitting(self):
        pass

    def initiate_data_ingestion(self):
        try:
            self.download_dataset_zip_file()
            #self.extract_tgz_file(tgz_file_path=tgz_file_path)
            #data_ingestion_artifact = self.split_data_as_train_test()
        except Exception as e:
            raise Exception(e, sys) from e