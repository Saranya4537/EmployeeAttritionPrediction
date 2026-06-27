import os
import joblib
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from src.logger import get_logger
from src.custom_exception import CustomException
from config.model_params import *

logger = get_logger()

class ModelTraining:
    def __init__(self, processed_input_path, model_output_path):
        self.processed_data_path = processed_input_path
        self.model_path = model_output_path
        self.clf = None
        self.X_train, self.X_test , self.y_train , self.y_test = None , None , None , None

        self.params_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS
        os.makedirs(self.model_path,exist_ok=True)
        logger.info("Model Training initialized...")

    def load_data(self):
        try:
            self.X_train = joblib.load(os.path.join(self.processed_data_path , "X_train.pkl"))
            self.X_test = joblib.load(os.path.join(self.processed_data_path , "X_test.pkl"))
            self.y_train = joblib.load(os.path.join(self.processed_data_path , "y_train.pkl"))
            self.y_test = joblib.load(os.path.join(self.processed_data_path , "y_test.pkl"))

            logger.info("Data loaded successfully...")

        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException("Failed to load data" , e)
        
    def train_model(self):
        try:
            logger.info("Intializing our model")
            lgbm = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            random_search = RandomizedSearchCV(
                estimator=lgbm,
                param_distributions=self.params_dist,
                n_iter = self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"]
            )
            logger.info("Starting our Hyperparamter tuning")

            random_search.fit(self.X_train,self.y_train)   

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_ 

            joblib.dump(best_lgbm_model,os.path.join(self.model_path , "model.pkl"))


            logger.info(f"Best paramters are : {best_params}")
            logger.info("Hyperparamter tuning completed")
            logger.info("Model trained and saved successfully...")

            return best_lgbm_model

        except Exception as e:
            logger.error(f"Error while training model {e}")
            raise CustomException("Failed to train model" , e)
        
    def evaluate_model(self,model):
        try:    
            logger.info("Evaluating the model") 
            y_pred = model.predict(self.X_test)
            accuracy = accuracy_score(self.y_test,y_pred)
            precision = precision_score(self.y_test,y_pred,average="weighted")
            recall = recall_score(self.y_test,y_pred,average="weighted")
            f1 = f1_score(self.y_test,y_pred,average="weighted")

            logger.info(f"Accuracy Score : {accuracy}")
            logger.info(f"Precision Score : {precision}")
            logger.info(f"Recall Score : {recall}")
            logger.info(f"F1 Score : {f1}")

            return {
            "accuracy" : accuracy,
            "precison" : precision,
            "recall" : recall,
            "f1" : f1
            }
        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException("Failed to evaluate model" ,  e)
        
    def run(self):
        self.load_data()
        best_model = self.train_model()
        self.evaluate_model(best_model)

if __name__=="__main__":
    trainer = ModelTraining("artifacts/processed/" , "artifacts/models/")
    trainer.run()        
    


    