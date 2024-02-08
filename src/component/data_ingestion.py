import os
import logging
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, config: DataIngestionConfig) -> None:
        """
        Initialize the DataIngestion instance.
        Args:
            config (DataIngestionConfig): Configuration for data ingestion.
        """
        self.config = config
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    def download_dataset(self):
        """
        Download the dataset from Kaggle.
        Returns:
            str: Path to the downloaded zip file.
        """
        try:
            logging.info("Downloading dataset from Kaggle...")
            api = KaggleApi()
            api.authenticate()
            dataset_url = self.config.kaggle_dataset_url
            zip_data_dir = self.config.zip_data_dir

            if os.path.exists(zip_data_dir):
                os.remove(zip_data_dir)

            os.makedirs(zip_data_dir, exist_ok=True)

            api.dataset_download_files(dataset=dataset_url, path=zip_data_dir, unzip=False)

            file_name = os.listdir(zip_data_dir)[0]
            zip_file_path = os.path.join(zip_data_dir, file_name)

            logging.info("Dataset downloaded successfully.")
            return zip_file_path

        except Exception as e:
            logging.error(f"Error downloading dataset: {str(e)}")
            raise e

    def extract_dataset(self, zip_file_path: str):
        """
        Extract the dataset from the zip file.
        Args:
            zip_file_path (str): Path to the zip file.
        Returns:
            str: Path to the extracted dataset.
        """
        try:
            extracted_data_dir = self.config.extracted_data_dir

            if os.path.exists(extracted_data_dir):
                os.remove(extracted_data_dir)

            os.makedirs(extracted_data_dir, exist_ok=True)

            logging.info("Extracting dataset...")
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(extracted_data_dir)

            dataset_name = os.listdir(extracted_data_dir)[0]
            dataset_path = os.path.join(extracted_data_dir, dataset_name)

            logging.info("Dataset extracted successfully.")
            return dataset_path

        except Exception as e:
            logging.error(f"Error extracting dataset: {str(e)}")
            raise e

    def ingest_data(self):
        """
        Ingest the data by downloading and extracting the dataset.
        Returns:
            DataIngestionArtifact: Artifact containing information about the ingestion process.
        """
        try:
            zip_file_path = self.download_dataset()
            dataset_path = self.extract_dataset(zip_file_path)
            artifact = DataIngestionArtifact(
                dataset_path=dataset_path,
                is_ingested=True,
                message="Data ingestion completed successfully."
            )
            return artifact

        except Exception as e:
            logging.error(f"Data ingestion failed: {str(e)}")
            raise e

    def initiate_data_ingestion(self):
        """
        Initiate the data ingestion process by downloading and extracting the dataset.
        Returns:
            DataIngestionArtifact: Artifact containing information about the ingestion process.
        """
        try:
            logging.info("Data ingestion process initiated.")
            artifact = self.ingest_data()
            logging.info("Data ingestion process completed.")
            return artifact

        except Exception as e:
            logging.error(f"Data ingestion process failed: {str(e)}")
            raise e
