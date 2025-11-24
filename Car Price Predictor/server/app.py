from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import sklearn
from xgboost import XGBRegressor
app = Flask(__name__)

# Load trained model
model = pickle.load(open("../model/model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Get form inputs
        car_details = {
            'name': request.form['name'],
            'year': int(request.form['year']),
            'km_driven': int(request.form['km_driven']),
            'fuel': request.form['fuel'],
            'seller_type': request.form['seller_type'],
            'transmission': request.form['transmission'],
            'owner': request.form['owner'],
            'mileage': float(request.form['mileage']),
            'engine': int(request.form['engine']),
            'max_power': float(request.form['max_power']),
            'seats': int(request.form['seats'])
        }


        # Create input vector (ordering and encoding should match training phase)
        input_df = pd.DataFrame([car_details])  # 👈 wrap dict in a list

        # Predict
        prediction = model.predict(input_df)[0]
        return render_template("app.html", prediction=round(prediction, 2))

    return render_template("app.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)