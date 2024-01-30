import os, sys
import logging
import zipfile

import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedShuffleSplit
from kaggle.api.kaggle_api_extended import KaggleApi

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    
    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'='*20}Data Ingestion log Started.{'='*20}\n\n")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Exception(e, sys) from e
        
    def download_dataset_zip_file(self):
        try:
            api = KaggleApi()
            api.authenticate()
            dataset_url = self.data_ingestion_config.kaggle_dataset_url
            zip_data_dir = self.data_ingestion_config.zip_data_dir

            if os.path.exists(zip_data_dir):
                os.remove(zip_data_dir)

            os.makedirs(zip_data_dir, exist_ok=True)

            api.dataset_download_files(dataset=dataset_url, path=zip_data_dir, unzip=False)

            file_name = os.listdir(zip_data_dir)[0]
            zip_file_path = os.path.join(zip_data_dir, file_name)

            return zip_file_path

        except Exception as e:
            raise Exception(e, sys)

    def extract_dataset(self, zip_file_path: str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            with zipfile.ZipFile(zip_file_path,"r") as zip_ref:
                zip_ref.extractall(raw_data_dir)
        except Exception as e:
            raise Exception(e, sys)

    def data_splitting(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            dataset_name = os.listdir(raw_data_dir)[0]
            raw_dataset_file_path = os.path.join(raw_data_dir, dataset_name)
            processed_data_dir = self.data_ingestion_config.processed_data_dir
            processed_train_dir = self.data_ingestion_config.processed_train_data_dir
            processed_test_dir = self.data_ingestion_config.processed_test_data_dir
            processed_train_file_path = os.path.join(processed_train_dir, dataset_name)
            processed_test_file_path = os.path.join(processed_test_dir, dataset_name)

            imdb_dataset = pd.read_csv(raw_dataset_file_path)

            imdb_dataset['score_cat'] = pd.cut(
                imdb_dataset["score"],
                bins = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0, 95.0, np.inf],
                labels = [1, 2, 3, 4, 5, 6, 7, 8]
            ).astype(float)

            imdb_dataset['score_cat'] = imdb_dataset['score_cat'].fillna(imdb_dataset.score_cat.median())

            strat_train_set = None
            start_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index, test_index in split.split(imdb_dataset, imdb_dataset['score_cat']):
                strat_train_set = imdb_dataset.loc[train_index].drop(['score_cat'], axis=1)
                strat_test_set = imdb_dataset.loc[test_index].drop(['score_cat'], axis=1)

            if strat_train_set is not None:
                os.makedirs(processed_train_dir, exist_ok=True)
                strat_train_set.to_csv(processed_train_file_path, index=False)
            
            if strat_test_set is not None:
                os.makedirs(processed_test_dir, exist_ok=True)
                strat_train_set.to_csv(processed_test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=processed_train_file_path,
                                                            test_file_path=processed_test_file_path,
                                                            is_ingested=True,
                                                            message=f"Data Ingestion Completed Successfully.")
            return data_ingestion_artifact
        except Exception as e:
            raise Exception(e, sys) from e

    def initiate_data_ingestion(self):
        try:
            zip_file_path = self.download_dataset_zip_file()
            self.extract_dataset(zip_file_path=zip_file_path)
            self.data_splitting()
        except Exception as e:
            raise Exception(e, sys) from e