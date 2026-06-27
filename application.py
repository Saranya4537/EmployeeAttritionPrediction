import joblib
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

MODEL_PATH = "C:/Users/kotha/OneDrive/Desktop/Saranya/DataScience/EmployeeAttritionPrediction/artifacts/models/model.pkl"
SCALAR_PATH = "C:/Users/kotha/OneDrive/Desktop/Saranya/DataScience/EmployeeAttritionPrediction/artifacts/processed/scaler.pkl"
loaded_model = joblib.load(MODEL_PATH)
scalar_model = joblib.load(SCALAR_PATH)

FEATURES = ['JobLevel','Shift','JobInvolvement','Age','TotalWorkingYears','YearsAtCompany','OverTime','YearsWithCurrManager','JobSatisfaction','MonthlyIncome']
LABELS = {
    0:'Leave',
    1:'Do not leave'
}

@app.route("/",methods=['GET','POST'])
def index():
    prediction = None
    print("inside index method")
    if request.method=='POST':
        try:
            input_data = [float(request.form[feature]) for feature in FEATURES]
            input_array = np.array(input_data).reshape(1,-1)


            print(input_array)
            scaled_array = scalar_model.transform(input_array)

            pred = loaded_model.predict(scaled_array)[0]
            prediction = LABELS.get(pred , "Unknown")

        except Exception as e:
            prediction = f"Error : {e}"    
    return render_template("index.html" , prediction=prediction , features = FEATURES)
    
            
if __name__=="__main__":
    app.run(debug=True)    