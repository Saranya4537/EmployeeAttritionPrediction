from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from config.model_params import *
from config.data_ingestion_config import *

if __name__ == "__main__":
    ###Data ingestion
    data_ingestion = DataIngestion(DATASET_NAME,TARGET_DIR)
    data_ingestion.run()

    ### 2. Data Processing
    processor = DataProcessing("artifacts/raw/watson_healthcare_modified.csv","artifacts/processed")
    processor.run()

    ### 3. Model Training
    trainer = ModelTraining("artifacts/processed/" , "artifacts/models/")
    trainer.run()
    
