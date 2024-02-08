import os, sys
import yaml

import pandas as pd


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Exception(e, sys) from e
    
def load_data(file_path:str) -> pd.DataFrame:
    try:
        dataframe = pd.read_csv(file_path)
        return dataframe
    except Exception as e:
        raise Exception(e, sys) from e
    
def save_data(data, file_path: str):
    try:
        data.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(e, sys) from e