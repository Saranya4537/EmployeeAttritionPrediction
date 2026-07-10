**About dataset:**<br>
The source of this dataset is kaggle.com. This dataset used to predict employee attrition. This dataset is taken from the hospital with employees of different roles.<br>
The data ingestion is done by importing the dataset from kagglehub.<br>
**Data processing:**<br>
data imbalance is corrected using SMOTE technique on the target variable<br>
Label encoding is done on columns with categorical features.<br>
Top 10 important features are selected using model.feature_importances_<br>
**Model Training:**<br>
lightgbm model is used to predict the employee attrition.
pipeline is created to orchestrate the process of data ingestion, data processing and model training and finally save the model using joblib and used to predict the saved model for user inputs.<br>
**User interface:**<br>
Flask is used to create the user interface for prediction based on the user inputs.<br>
**CI CD Deployment:**<br>
It is a powerful automation server used to implement the entire CI/CD (Continuous Integration and Continuous Delivery/Deployment) pipeline. It automates the process of building, testing, and deploying your software. <br>
**Continuous Integration (CI):** Automatically pulling code from a repository, compiling it, and running automated tests to ensure new code merges safely.<br>
**Continuous Delivery/Deployment (CD):** Automatically deploying the tested application to staging or production environments<br>
setup a Jenkins container and this is called docker in docker<br>
github integration with jenkins<br>
dockerization of the project<br>
Create a virtual environment in your jenkins container<br>
Build docker image of the project<br>
Push the docker image into Artifacts registry in GCP. Artifacts registry acts like a docker hub<br>
Extract the image from artifacts registry and push to Google cloud run.<br>
All these steps are mentioned as pipelines with stages in Jenkinsfile.<br>
Now the app is deployed using GCP console<br>






