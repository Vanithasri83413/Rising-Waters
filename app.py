from flask import Flask, render_template, request, redirect, url_for
import joblib
import pandas as pd
import numpy as np

# 1. Initialize the Flask App instance
app = Flask(__name__)

# 2. Load the production-ready machine learning assets we saved in Epic 4
try:
    model = joblib.load('floods.save')
    scaler = joblib.load('transform.save')
    print("🚀 SUCCESS: Loaded 'floods.save' and 'transform.save' assets into memory.")
except Exception as e:
    print(f"⚠️ ERROR LOADING ASSETS: {e}. Make sure the .save files are in the root directory.")

# 3. Setup Page Routing
@app.route('/')
@app.route('/home')
def home():
    # Landing page explaining the project
    return render_template('home.html')

# We add both routes here so your navigation bar connects perfectly!
@app.route('/predict')
@app.route('/predict_form')
@app.route('/index')
def predict_form():
    # Input form for climate metrics
    return render_template('index.html')

# 4. Handle Live User Submission / Prediction Logic
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Gather the 5 user inputs directly from the submitted web form fields
            cloud_cover = float(request.form['cloud_cover'])
            annual_rainfall = float(request.form['annual_fallback'])
            jan_feb = float(request.form['jan_feb'])
            mar_may = float(request.form['mar_may'])
            jun_sep = float(request.form['jun_sep'])
            
            # Combine form values into an explicit structure matching our dataset training shape
            raw_features = np.array([[cloud_cover, annual_rainfall, jan_feb, mar_may, jun_sep]])
            
            # Apply standard scaling using our saved metrics
            scaled_features = scaler.transform(raw_features)
            
            # Execute model inference via our trained gradient booster
            prediction = model.predict(scaled_features)
            
            # Route users dynamically based on prediction status (0: Safe, 1: Flood Risk)
            if prediction[0] == 1:
                return render_template('chance.html')
            else:
                return render_template('no_chance.html')
                
        except Exception as err:
            return f"❌ Server Process Error: {err}. Ensure all form parameters match numeric conditions."

# 5. Start development local server
if __name__ == '__main__':
    # Launch on localhost
    app.run(debug=True, port=5000)
    