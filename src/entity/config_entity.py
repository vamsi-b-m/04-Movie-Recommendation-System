from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["kaggle_dataset_url", "zip_data_dir", "raw_data_dir", "ingested_data_dir", "ingested_train_data_dir", "ingested_test_data_dir"])
TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])