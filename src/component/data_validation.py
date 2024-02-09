import os
import sys
import json
import logging
import pandas as pd

from src.constant import *
from src.utils import load_data, read_yaml_file
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataCleaningArtifact, DataValidationArtifact

class DataValidation:
    
    def __init__(self, data_validation_config:DataValidationConfig, data_cleaning_artifact:DataCleaningArtifact) -> None:
        try:
            self.data_validation_config = data_validation_config
            self.data_cleaning_artifact = data_cleaning_artifact
            self.schema_info = read_yaml_file(self.data_validation_config.schema_file_path)
            self.logger = logging.getLogger(__name__)
            self.validation_results = {'null_values': None, 'duplicates': None, 'inconsistency_indices': None, 'schema_feature_missing': None, 'dataset_feature_extra': None, 'schema_feature_not_in_dataset': None, 'schema_feature_dtype_mismatch': None}
        except Exception as e:
            raise Exception(e,sys) from e

    def read_data(self):
        try:
            cleaned_data_file_path = self.data_cleaning_artifact.cleaned_data_file_path
            self.data = load_data(file_path=cleaned_data_file_path)
            self.logger.info("Data loaded successfully from %s", cleaned_data_file_path)
        except Exception as e:
            self.logger.exception("Error occurred while reading data", exc_info=True)
            raise

    def check_null_values(self) -> bool:
        try:
            validate_null_values = False
            rows_with_null = self.data[self.data.isnull().any(axis=1)]
            if not rows_with_null.empty:
                self.validation_results['null_values'] = list(rows_with_null.index)
                self.logger.info("Rows with null values found : %s", self.validation_results['null_values'])
            else:
                self.logger.info("No rows with null values found.")
                validate_null_values = True
            return validate_null_values
        except Exception as e:
            raise Exception(e, sys) from e

    def check_duplicates(self) -> bool:
        try:
            validate_duplicates = False
            duplicates = self.data[self.data.duplicated()]
            if not duplicates.empty:
                self.validation_results['duplicates'] = list(duplicates.index)
                self.logger.info("Duplicates found : %s", self.validation_results['duplicates'])
            else:
                self.logger.info("No duplicates found.")
                validate_duplicates = True
            return validate_duplicates
        except Exception as e:
            raise Exception(e, sys) from e
    
    def check_consistency(self) -> bool:
        try:
            validate_consistency = False
            inconsistency_indices = [str(self.data.index[i]) + " Missing" for i in range(1, len(self.data.index)) if self.data.index[i] != self.data.index[i-1] + 1]
            if inconsistency_indices:
                self.validation_results['inconsistency_indices'] = inconsistency_indices
                self.logger.info("Inconsistency found at the indexes : %s", self.validation_results['inconsistency_indices'])
            else:
                self.logger.info("No inconsistency found.")
                validate_consistency = True
            return validate_consistency
        except Exception as e:
            raise Exception(e, sys) from e
        
    def check_outliers(self) -> bool:
        try:
            pass
        except Exception as e:
            raise Exception(e, sys) from e

    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False
            schema_features = list(self.schema_info['columns'].keys())
            dataset_features = list(self.data.columns)

            if len(schema_features) > len(dataset_features):
                self.validation_results['schema_feature_missing'] = [feature for feature in schema_features if feature not in dataset_features]
                self.logger.info("Some features which are in schema are not found in dataset.")
            elif len(dataset_features) > len(schema_features):
                self.validation_results['dataset_feature_extra'] = [feature for feature in dataset_features if feature not in schema_features]
                self.logger.info("Some features which are not in schema are found in dataset.")
            else:
                for feature in schema_features:
                    if feature not in dataset_features:
                        self.validation_results['schema_feature_not_in_dataset'] = feature
                        self.logger.info("Feature %s not found in the dataset.", feature)
                    else:
                        if not self.schema_info['columns'][feature] == self.data[feature].dtype.name:
                            self.validation_results['schema_feature_dtype_mismatch'] = feature
                            self.logger.info("schema feature %s has different dtype when compared to dataset feature %s dtype.", feature, feature)
                else:
                    validation_status = True
                    self.logger.info("All the features which are mentioned in the schema are available in dataset.")

            return validation_status 
        except Exception as e:
            raise Exception(e, sys) from e

    def get_and_save_data_validation_report(self):
        try:
            report_file_dir = self.data_validation_config.report_file_dir
            report_file_path = self.data_validation_config.report_file_path
            os.makedirs(report_file_dir, exist_ok=True)
            with open(report_file_path, 'w') as report_file:
                json.dump(self.validation_results, report_file, indent=4)
        except Exception as e:
            raise Exception(e, sys) from e

    def initiate_data_validation(self):
        try:
            self.logger.info("Data Validation Process Started.")
            self.read_data()
            self.check_null_values()
            self.check_duplicates()
            self.check_consistency()
            self.validate_dataset_schema()
            self.get_and_save_data_validation_report()
            self.logger.info("Data Validation Process Completed.\n")
        except Exception as e:
            raise Exception(e, sys) from e
