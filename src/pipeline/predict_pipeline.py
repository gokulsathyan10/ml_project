import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig


class PredictPipeline:
    def predict(self, features: pd.DataFrame):
        try:
            preprocessor_path = DataTransformationConfig().preprocessor_obj_file_path
            model_path = ModelTrainerConfig().trained_model_file_path

            logging.info("Loading preprocessor and model")
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            features_scaled = preprocessor.transform(features)
            predictions = model.predict(features_scaled)
            logging.info("Prediction completed")
            return predictions

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        writing_score: int,
        reading_score: int,
    ):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.writing_score = writing_score
        self.reading_score = reading_score

    def get_data_as_dataframe(self) -> pd.DataFrame:
        try:
            data = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "writing_score": [self.writing_score],
                "reading_score": [self.reading_score],
            }
            return pd.DataFrame(data)

        except Exception as e:
            raise CustomException(e, sys)
