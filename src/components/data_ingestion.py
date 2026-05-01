import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from typing import Iterable, Tuple

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")
    input_data_path: str=os.path.join('notebooks','data','stud.csv')
    supported_exts: Tuple[str, ...]=(".csv", ".parquet", ".pq", ".xlsx", ".xls", ".json", ".jsonl")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def _find_input_file(self, path: str, exts: Iterable[str]) -> str:
        if os.path.isdir(path):
            for name in sorted(os.listdir(path)):
                full = os.path.join(path, name)
                if os.path.isfile(full) and name.lower().endswith(tuple(exts)):
                    return full
            raise FileNotFoundError(f"No supported data files found in directory: {path}")
        return path

    def _load_dataframe(self, path: str) -> pd.DataFrame:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            return pd.read_csv(path)
        if ext in (".parquet", ".pq"):
            return pd.read_parquet(path)
        if ext in (".xlsx", ".xls"):
            return pd.read_excel(path)
        if ext in (".json", ".jsonl"):
            # jsonl is line-delimited JSON
            lines = ext == ".jsonl"
            return pd.read_json(path, lines=lines)
        raise ValueError(f"Unsupported file extension: {ext}")

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            path = self._find_input_file(
                self.ingestion_config.input_data_path,
                self.ingestion_config.supported_exts,
            )
            df=self._load_dataframe(path)
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Inmgestion of the data iss completed")

    

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                

            )
        except Exception as e:
            raise CustomException(e,sys)
        


