# 1. Data Collection
# 2. Data Ingestion
# 3. Data Validation
# 4. Data Visualization
# 5. Model Initialization
# 6. Model Evaluation
# 7. Model Push
import os, sys
from src.constant import *
from src.utils import *
from src.constant import *
from kaggle.api.kaggle_api_extended import KaggleApi
from src.configuration.configuration import Configuration
from src.component.data_ingestion import DataIngestion
from src.pipeline.pipeline import Pipeline


def hell():
    pipeline = Pipeline()
    pipeline.start_data_ingestion()


if __name__=="__main__":
    hell()