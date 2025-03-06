import joblib
import numpy as np

# Load trained model & scaler
model = joblib.load("aqi_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_aqi(pm2_5, pm10, co, no2):
    input_data = np.array([[pm2_5, pm10, co, no2]])
    input_scaled = scaler.transform(input_data)
    predicted_aqi = model.predict(input_scaled)
    print(f"Predicted AQI: {predicted_aqi[0]:.2f}")

# Test with a sample city
predict_aqi(50, 80, 400, 10)  # Replace with real fetched data
