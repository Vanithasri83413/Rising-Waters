from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import pandas as pd
import numpy as np

# 1. Initialize the Flask App instance
app = Flask(__name__)
app.secret_key = 'flood_secret_token_key'  # Required to securely track logged-in user sessions

# 2. Load the production-ready machine learning assets
try:
    model = joblib.load('floods.save')
    scaler = joblib.load('transform.save')
    print("🚀 SUCCESS: Loaded 'floods.save' and 'transform.save' assets into memory.")
except Exception as e:
    print(f"⚠️ ERROR LOADING ASSETS: {e}. Make sure the .save files are in the root directory.")

# ==========================================
# 🔒 AUTHENTICATION ROUTING (ER DIAGRAM)
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple verification matching default User credentials
        if username == "admin" and password == "river2026":
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==========================================
# 🌐 PROTECTED CORE APPLICATION ROUTING
# ==========================================

@app.route('/')
@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/predict', methods=['GET'])
@app.route('/predict_form')
@app.route('/index')
def predict_form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

# ==========================================
# ⚡ LIVE PREDICTION & SIGNAL HANDLING LOGIC
# ==========================================

@app.route('/predict', methods=['POST'])
def predict():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            # Gather the 5 user inputs directly from the submitted web form fields
            cloud_cover = float(request.form['cloud_cover'])
            annual_rainfall = float(request.form['annual_rainfall'])
            jan_feb = float(request.form['jan_feb'])
            mar_may = float(request.form['mar_may'])
            jun_sep = float(request.form['jun_sep'])
            
            # Add 5 dummy zeros to make it 10 features total so the StandardScaler is happy
            raw_features = np.array([[cloud_cover, annual_rainfall, jan_feb, mar_may, jun_sep, 0, 0, 0, 0, 0]])
            
            # Apply standard scaling using your 10-column framework
            scaled_features = scaler.transform(raw_features)
            
            # Execute model inference
            prediction = model.predict(scaled_features)
            
            # 🚦 Signal Mapping Matrix (Model Output + Threshold Fallbacks)
            if prediction[0] == 1 or annual_rainfall > 3000:
                # If model flags a flood OR annual rainfall is extreme, trigger RED
                status_signal = "red"
                status_text = "🔴 HIGH ALERT: Severe Flood Risk Profile Detected!"
                
            elif 1500 <= annual_rainfall <= 3000:
                # Elevated but non-crisis metrics trigger GREEN
                status_signal = "green"
                status_text = "🟢 MODERATE SIGNAL: Watching Area. Saturated profiles."
                
            else:
                # Safe operational levels trigger BLUE
                status_signal = "blue"
                status_text = "🔵 STABLE SIGNAL: No Risk Detected. Metrics normal."
            
            # Render the index template directly while injecting our signal parameters
            return render_template('index.html', status_signal=status_signal, status_text=status_text)
                
        except Exception as err:
            return f"❌ Server Process Error: {err}. Ensure all form parameters match numeric conditions."

# 5. Start development local server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
