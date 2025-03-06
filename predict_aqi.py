import joblib
import numpy as np

# Load the trained model
model = joblib.load("aqi_predictor.pkl")

# Function to predict AQI
def predict_aqi(temperature, humidity, wind_speed, traffic_density):
    input_data = np.array([[temperature, humidity, wind_speed, traffic_density]])
    predicted_aqi = model.predict(input_data)[0]
    return round(predicted_aqi, 2)

# Example usage
temperature = float(input("Enter temperature (°C): "))
humidity = float(input("Enter humidity (%): "))
wind_speed = float(input("Enter wind speed (km/h): "))
traffic_density = float(input("Enter traffic density: "))

predicted_aqi = predict_aqi(temperature, humidity, wind_speed, traffic_density)
print(f"\n🔹 Predicted AQI: {predicted_aqi}")
