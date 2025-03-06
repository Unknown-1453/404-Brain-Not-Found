import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load dataset
data = pd.read_csv(r"C:\Users\sinch\OneDrive\Music\Desktop\Hack\aqi_data.csv")
print("Dataset loaded successfully!")

# Check if required columns exist
required_columns = {"PM2.5", "PM10", "CO", "NO2", "AQI"}
if not required_columns.issubset(data.columns):
    raise ValueError(f"Dataset is missing required columns: {required_columns - set(data.columns)}")

# Step 2: Prepare features (X) and target (y)
X = data[["PM2.5", "PM10", "CO", "NO2"]]  # Features
y = data["AQI"]  # Target variable

# Step 3: Split into training & testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Standardize Data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 5: Train Model
model = LinearRegression()
model.fit(X_train_scaled, y_train)
print("✅ Model training completed!")

# Step 6: Evaluate Model
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.4f}")

# Avoid UndefinedMetricWarning for R²
if len(y_test) > 1:
    r2 = r2_score(y_test, y_pred)
    print(f"R² Score: {r2:.4f}")
else:
    print("⚠️ Warning: R² score is not well-defined for less than two samples.")

# Save the trained model and scaler
with open("aqi_model.pkl", "wb") as f:
    joblib.dump(model, f)
with open("scaler.pkl", "wb") as f:
    joblib.dump(scaler, f)

print("✅ Model saved successfully as 'aqi_model.pkl' and 'scaler.pkl'!")
