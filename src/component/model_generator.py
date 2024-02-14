import os
import sys
import csv
import logging

import pandas as pd

from src.utils import load_data
from src.entity.config_entity import ModelGeneratorConfig
from src.entity.artifact_entity import DataManipulationArtifact, ModelTrainingArtifact

class ModelGenerator:

    def __init__(self, model_generation_config: ModelGeneratorConfig, data_manipulation_artifact: DataManipulationArtifact) -> None:
        try:
            self.model_generation_config = model_generation_config
            self.data_manipulation_artifact = data_manipulation_artifact
            self.similarity = self.data_manipulation_artifact.similarity
            self.logger = logging.getLogger(__name__)
            self.logger.info("ModelTrainer initialized.")
        except Exception as e:
            self.logger.error(f"Error initializing ModelTrainer: {e}")
            raise Exception(e, sys) from e

    def read_data(self):
        try:
            processed_data_file_path = self.data_manipulation_artifact.processed_data_file_path
            self.logger.info(f"Reading data from file: {processed_data_file_path}")
            self.processed_data = load_data(file_path=processed_data_file_path)
            self.logger.info("Data read successfully.")
        except Exception as e:
            self.logger.error(f"Error reading data: {e}")
            raise Exception(e, sys) from e

    def recommend_with_movie_name(self, movie_name, movie_count_to_recommend):
        try:
            movies_recommended = []
            self.logger.info(f"Recommendation based on movie name: {movie_name}")
            index = self.processed_data[self.processed_data['names']==movie_name].index[0]
            distances = sorted(list(enumerate(self.similarity[index])), reverse=True, key=lambda vector: vector[1])
            for i in distances[0:movie_count_to_recommend]:
                movies_recommended.append(self.processed_data.iloc[i[0]].names)
            return movies_recommended
        except Exception as e:
            self.logger.error(f"Error recommending with movie name: {e}")
            raise Exception(e, sys) from e

    def recommend_with_genre(self, target_genre):
        try:
            self.logger.info("Initiating recommendation based on genre.")
            # Define start column index and target genre
            start_column_index = 3
            movie_names = []
            
            for movie_index in range(len(self.processed_data)):
                movie_row = self.processed_data.iloc[movie_index, start_column_index:]
                if movie_row[target_genre] and not movie_row[movie_row.index != target_genre].any():
                    movie_names.append(self.processed_data.iloc[movie_index]['names'])

            movie_count = len(movie_names)
            self.logger.info(f"Only {movie_count} movies are available based on genre : {target_genre}")
            if movie_count < 15:
                movies_to_recommend_count = 15 - movie_count
                self.logger.info(f"Started recommend_with_movie_name to fetch movies based on the first movie from genre movie list")
                recommended_movies_by_name = self.recommend_with_movie_name(movie_names[0], movies_to_recommend_count)
                movies_recommended = movie_names + recommended_movies_by_name
                self.logger.info(f"Recommended movies based on genre: {movies_recommended}")
            else:
                movies_recommended = movie_names[:15]
                self.logger.info(f"Recommended movies based on genre: {movies_recommended}")
            return movies_recommended
        except Exception as e:
            error_message = f"Error recommending with genre: {e}"
            self.logger.error(error_message)
            raise Exception(error_message) from e

    def get_movie_recommendation(self, movie_name, target_genre):
        try:
            recommended_movies = []
            if movie_name:
                self.logger.info("Recommending based on the Movie name : %s", movie_name)
                recommended_movies = self.recommend_with_movie_name(movie_name=movie_name, movie_count_to_recommend=15)
            elif target_genre:
                self.logger.info("Recommending based on the Movie Genre : %s", target_genre)
                recommended_movies = self.recommend_with_genre(target_genre=target_genre)
            else:
                pass

            self.logger.info("Model training process completed.")
            return recommended_movies 

        except Exception as e:
            raise Exception(e, sys) from e
        
    def write_to_csv(self, recommended_movies):
        try:
            model_generated_data_dir = self.model_generation_config.model_generated_data_dir
            os.makedirs(model_generated_data_dir, exist_ok=True)
            model_generated_data_file_path = self.model_generation_config.model_generated_data_file_path

            # Check if file exists
            if not os.path.isfile(model_generated_data_file_path):
                # If file does not exist, create it with column names
                header = [f"Movie-{i}" for i in range(1, 16)]  # Column names Movie-1, Movie-2, ..., Movie-15
                df = pd.DataFrame(columns=header)
                df.to_csv(model_generated_data_file_path, index=True)
            
            # Append data to the CSV file
            df = pd.DataFrame([recommended_movies])
            df.to_csv(model_generated_data_file_path, mode='a', header=False, index=True)

            self.logger.info(f"Successfully wrote recommended movies to CSV: {model_generated_data_file_path}")
            return model_generated_data_file_path
        except Exception as e:
            error_msg = f"Error occurred while writing recommended movies to CSV: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg) from e

    def initiate_model_training(self):
        try:
            movie_name = input("Movie Name : ")
            target_genre = input("Target Name : ")
            self.logger.info("Initiating model training process.")
            self.read_data()
            recommended_movies = self.get_movie_recommendation(movie_name=movie_name, target_genre=target_genre)
            model_generated_data_file_path = self.write_to_csv(recommended_movies=recommended_movies)
            self.logger.info("Model training completed successfully.")
            model_training_artifact = ModelTrainingArtifact(model_generated_data_file_path=model_generated_data_file_path)
            return model_training_artifact
        except Exception as e:
            error_msg = f"Error during model training: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg) from e
