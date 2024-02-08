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
from src.pipeline.pipeline import Pipeline


def hell():
    pipeline = Pipeline()
    pipeline.run_pipeline()


if __name__=="__main__":
    hell()