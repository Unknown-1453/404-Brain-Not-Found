import requests
import pandas as pd
import time

# OpenWeather API Key
API_KEYS = ["5841e4968d530deb5e2ce0edbbfc8339", "1b1a275ffabba6dbb5ee23f2289bb7ef", "0de7d82479dc3111d395112cd0443eab","3860976cd3d721b01da00872884b6cca"]  # Add multiple API keys to avoid limits
key_index = 0  # Start with the first API key

# List of cities to fetch AQI data for
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]

# Function to get latitude and longitude of a city
def get_lat_lon(city):
    global key_index
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEYS[key_index]}"
    response = requests.get(geo_url).json()
    
    if response:
        return response[0]["lat"], response[0]["lon"]
    else:
        print(f"❌ Could not get location for {city}")
        return None, None

# Function to fetch AQI data
def get_aqi_data(lat, lon):
    global key_index
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEYS[key_index]}"
    response = requests.get(aqi_url).json()
    
    if "list" in response and len(response["list"]) > 0:
        aqi_info = response["list"][0]
        return {
            "AQI": aqi_info["main"]["aqi"],
            "PM2.5": aqi_info["components"]["pm2_5"],
            "PM10": aqi_info["components"]["pm10"],
            "CO": aqi_info["components"]["co"],
            "NO2": aqi_info["components"]["no2"]
        }
    else:
        print("⚠️ No AQI data available.")
        return None

# Collect data and store it in a DataFrame
aqi_data = []

for city in cities:
    lat, lon = get_lat_lon(city)
    if lat and lon:
        aqi_details = get_aqi_data(lat, lon)
        if aqi_details:
            aqi_details["City"] = city
            aqi_data.append(aqi_details)
    
    time.sleep(1)  # Add delay to avoid rate limits

# Save data to CSV file
df = pd.DataFrame(aqi_data)
df.to_csv("aqi_data.csv", index=False)
print("✅ AQI data saved to aqi_data.csv")
