import kagglehub
import os
import shutil
from src.logger import get_logger
from src.custom_exception import CustomException
from config.data_ingestion_config import *

logger = get_logger()

class DataIngestion:

    def __init__(self,dataset_name:str , target_dir:str):
        self.dataset_name = dataset_name
        self.target_dir = target_dir

    def create_rawdir(self):
        try:
            raw_dir = os.path.join(self.target_dir,"raw")
            if not os.path.exists(raw_dir):
                os.makedirs(raw_dir)
                logger.info("Raw directory created successfully.") 
            raw_dir = raw_dir + "\\"
            return raw_dir       
        except Exception as e:
                logger.error(f"Error occurred while creating raw directory: {e}")
                raise CustomException(f"Error occurred while creating raw directory: {e}", e)       
        
    def download_dataset(self):
        try:
            logger.info("Downloading dataset from Kaggle...") 
            path = kagglehub.dataset_download(self.dataset_name)
            logger.info(f"Dataset downloaded to: {path}") 
            source_file_path = os.path.join(path, FILE_NAME)
            return source_file_path         
        except Exception as e:
            logger.error(f"Error occurred while downloading dataset: {e}")
            raise CustomException(f"Error occurred while downloading dataset: {e}",e)  

    def move_file(self, file_path:str, raw_dir:str):
        try:
            if(os.path.exists(file_path)):
                logger.info(f"Source file path is {file_path}") 
                shutil.move(file_path,raw_dir)
                logger.info(f"Dataset downloaded and moved to {raw_dir}") 
        except Exception as e:
            logger.error(f"Error occurred while moving dataset file: {e}")
            raise CustomException(f"Error occurred while moving dataset file: {e}", e)             

    def run(self):
        try:
            raw_dir = self.create_rawdir()
            file_path = self.download_dataset()
            self.move_file(file_path, raw_dir)
        except Exception as e:
            logger.error(f"Error occurred during data ingestion: {e}")
            raise CustomException(f"Error occurred during data ingestion: {e}", e)
            
if __name__=="__main__":
     data_ingestion = DataIngestion(DATASET_NAME,TARGET_DIR)
     data_ingestion.run()
