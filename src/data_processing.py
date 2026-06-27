import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
from src.custom_exception import CustomException
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
import src.logger as lg
import joblib

logger = lg.get_logger()

class DataProcessing:


    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

        os.makedirs(self.output_path,exist_ok=True)
        logger.info("Data processing initialized")


    def load_data(self):
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info("Data loaded successfully for processing")

        except Exception as e:
            logger.error(f"Error while loading the file {e}")
            raise CustomException("Failed to load data", e)

    def label_encode(self):
        try:
            categorical=[]
            numerical=[]
            for col in self.df.columns:
                if self.df[col].dtype == 'str':
                    categorical.append(col) 
                else:
                    numerical.append(col)

            for col in categorical:
                label_encoder = LabelEncoder()
                self.df[col] = label_encoder.fit_transform(self.df[col])
                label_mapping = dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))                    
                logger.info(f"Label mapping for {col}")
                logger.info(label_mapping)

            logger.info("Label encoding completed")    
            print("Inside label encoding")
            print(self.df.shape)
            return self.df

        except Exception as e:    
            logger.error(f"Error in label encoding of categorical variables {e}")
            raise CustomException("Failed to label encode the catgorical columns", e)

    def balancing_data(self,df):
        try:
            logger.info("Balancing data")
            X = df.drop(columns='Attrition')
            y = df["Attrition"]

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X,y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["Attrition"]=y_resampled

            logger.info("Data imbalance handled successfully")
            print("inside balancing data")
            print(balanced_df.shape)
            return balanced_df

        except Exception as e:
            logger.error(f"Error while balancing data {e}")
            raise CustomException("Failed to balance the data", e)        
        
    def select_features(self,df):
        try:
            logger.info("Feature selection in process")
            X = df.drop(columns='Attrition')
            y = df["Attrition"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance =  model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature':X.columns,
                'importance':feature_importance
            })

            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            num_of_features_to_select = 10

            top_10_features = top_features_importance_df["feature"].head(num_of_features_to_select).values

            logger.info(f"Features selected : {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ["Attrition"]]
            print("inside select features method")
            print(top_10_df.shape)
            
            logger.info("Feature slection completed successfully")
            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during feature selection step {e}")
            raise CustomException("Error while feature selection", e)

           
    def split_data(self,df):
        try:
            X=df.drop('Attrition',axis=1)    
            Y=df["Attrition"]
            print("inside split data method")
            print(X.shape)

            logger.info(X.columns)
            X_train , X_test , y_train , y_test = train_test_split(X,Y , test_size=0.2 , random_state=42)
            joblib.dump(X_train , os.path.join(self.output_path , "X_train.pkl"))
            joblib.dump(X_test , os.path.join(self.output_path , "X_test.pkl"))
            joblib.dump(y_train , os.path.join(self.output_path , "y_train.pkl"))
            joblib.dump(y_test , os.path.join(self.output_path , "y_test.pkl"))

            logger.info("Splitted and saved sucesfully....")        

        except Exception as e:   
            logger.error(f"Error while dropping columns {e}")
            raise CustomException("Failed to drop the columns", e)    



    def run(self):
        self.load_data()
        encoded_df = self.label_encode()
        balanced_df = self.balancing_data(encoded_df)
        df_with_imp_features = self.select_features(balanced_df)
        print(df_with_imp_features.shape)
        self.split_data(df_with_imp_features)

        logger.info("Data processing completed")


if __name__=="__main__":
    processor = DataProcessing("artifacts/raw/watson_healthcare_modified.csv","artifacts/processed")
    processor.run()

