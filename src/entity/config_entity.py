from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["kaggle_dataset_url", "zip_data_dir", "ingested_data_dir"])
DataCleaningConfig = namedtuple("DataCleaningConfig", ["cleaned_data_dir", "cleaned_data_file_path"])
DataValidationConfig = namedtuple("DataValidationConfig", ["schema_file_path", "report_file_path", "report_page_file_path"])
DataManipulationConfig = namedtuple("DataManipulationConfig", ["processed_data_dir", "processed_pickle_data_dir"])
TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])