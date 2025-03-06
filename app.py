from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model & scaler
model = joblib.load("aqi_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    pm2_5 = data["PM2.5"]
    pm10 = data["PM10"]
    co = data["CO"]
    no2 = data["NO2"]

    input_data = np.array([[pm2_5, pm10, co, no2]])
    input_scaled = scaler.transform(input_data)
    predicted_aqi = model.predict(input_scaled)

    return jsonify({"Predicted AQI": round(predicted_aqi[0], 2)})

if __name__ == "__main__":
    app.run(debug=True)
