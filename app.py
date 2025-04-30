# from flask import Flask, request, render_template
# import pandas as pd
# import joblib

# app = Flask(__name__)

# # Load the pre-trained model and preprocessor
# model = joblib.load('models/model.pkl')
# preprocessor = joblib.load('models/preprocessor.pkl')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Extract input values from the form
#         dep_time = request.form['Dep_Time']
#         arrival_time = request.form['Arrival_Time']
#         source = request.form['Source']
#         destination = request.form['Destination']
#         stops = request.form['stops']
#         airline = request.form['airline']

#         # Parse departure time
#         dep_time_obj = pd.to_datetime(dep_time, format='%Y-%m-%dT%H:%M')
#         dep_hour = dep_time_obj.hour
#         dep_minute = dep_time_obj.minute

#         # Create DataFrame for prediction
#         input_data = pd.DataFrame({
#             'Journey_day': [dep_time_obj.day],
#             'Journey_month': [dep_time_obj.month],
#             'Dep_hour': [dep_hour],
#             'Dep_min': [dep_minute],
#             'Source': [source],
#             'Destination': [destination],
#             'Airline': [airline],
#             'Total_Stops': [stops],
#         })

#         # Apply preprocessing (encoding categorical features)
#         input_data_transformed = preprocessor.transform(input_data)

#         # Ensure the transformed data is 2D
#         if input_data_transformed.ndim == 1:
#             input_data_transformed = input_data_transformed.reshape(1, -1)

#         # Make prediction
#         prediction = model.predict(input_data_transformed)
#         prediction = prediction.flatten()[0]

#         return render_template('index.html', prediction_text=f'Predicted Price: ₹{prediction:.2f}')

#     except Exception as e:
#         return render_template('index.html', prediction_text=f'Error: {str(e)}')

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=8080)



import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Load pre-trained model and preprocessor
model = joblib.load('models/model.pkl')
preprocessor = joblib.load('models/preprocessor.pkl')

# Streamlit App Title
st.title("Flight Fare Prediction App ✈️")

# Input fields
st.subheader("Enter Flight Details")

dep_date = st.date_input("Departure Date", value=datetime.now().date())
dep_clock = st.time_input("Departure Time", value=datetime.now().time())
dep_time = datetime.combine(dep_date, dep_clock)

arrival_time = st.time_input("Arrival Time")  # Not used in prediction currently

source = st.selectbox("Source", ["Delhi", "Kolkata", "Mumbai", "Chennai", "Banglore"])
destination = st.selectbox("Destination", ["Cochin", "Delhi", "New Delhi", "Hyderabad", "Kolkata", "Banglore"])
airline = st.selectbox("Airline", ["IndiGo", "Air India", "Jet Airways", "SpiceJet", "Vistara", "GoAir", "Multiple carriers"])
stops = st.selectbox("Total Stops", ["non-stop", "1 stop", "2 stops", "3 stops", "4 stops"])

# Prediction Button
if st.button("Predict Price"):
    try:
        # After all inputs are taken
        stops_mapping = {
            "non-stop": 0,
            "1 stop": 1,
            "2 stops": 2,
            "3 stops": 3,
            "4 stops": 4
                }
        stops_int = stops_mapping.get(stops, 0)

        input_data = pd.DataFrame({
            'Journey_day': [dep_time.day],
            'Journey_month': [dep_time.month],
            'Dep_hour': [dep_time.hour],
            'Dep_min': [dep_time.minute],
            'Source': [source],
            'Destination': [destination],
            'Airline': [airline],
            'Total_Stops': [stops_int]
            })


        # Preprocessing
        input_data_transformed = preprocessor.transform(input_data)

        # Make prediction
        prediction = model.predict(input_data_transformed)
        prediction = prediction.flatten()[0]

        # Show result
        st.success(f"Predicted Flight Price: ₹{prediction:.2f}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
