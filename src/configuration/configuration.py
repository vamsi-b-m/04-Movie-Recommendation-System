import os, sys
from src.constant import *
from src.utils import *
from src.constant import *
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from kaggle.api.kaggle_api_extended import KaggleApi



class Configuration:

    def __init__(self, config_file_path:str=CONFIG_FILE_PATH, current_time_stamp:str=CURRENT_TIME_STAMP) -> None:
        try:
            self.config_file_path = config_file_path
            self.config_info = read_yaml_file(file_path=self.config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise Exception(e, sys) from e
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        artifact_dir = self.training_pipeline_config.artifact_dir
        data_ingestion_artifact_dir = os.path.join(
            artifact_dir,
            self.time_stamp,
            DATA_INGESTION_ARTIFACT_DIR
        )
        data_ingestion_config_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
        kaggle_dataset_url = data_ingestion_config_info[DATA_INGESTION_KAGGLE_DATASET_URL_KEY]
        zip_data_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_ZIP_DATA_DIR_KEY])
        raw_data_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR_KEY])
        ingested_data_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_INGESTED_DATA_DIR])
        ingested_train_data_dir = os.path.join(data_ingestion_artifact_dir, ingested_data_dir, data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DATA_DIR])
        ingested_test_data_dir = os.path.join(data_ingestion_artifact_dir, ingested_data_dir, data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DATA_DIR])

        data_ingestion_config = DataIngestionConfig(kaggle_dataset_url=kaggle_dataset_url,
                                                    zip_data_dir=zip_data_dir,
                                                    raw_data_dir=raw_data_dir,
                                                    ingested_data_dir=ingested_data_dir,
                                                    ingested_train_data_dir=ingested_train_data_dir,
                                                    ingested_test_data_dir=ingested_test_data_dir
                                                    )
        return data_ingestion_config

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
        artifact_dir = os.path.join(ROOT_DIR , DATA_DIR, training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
        training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
        return training_pipeline_config