import requests
import csv
import time

API_KEYS = ["5841e4968d530deb5e2ce0edbbfc8339", "1b1a275ffabba6dbb5ee23f2289bb7ef", "0de7d82479dc3111d395112cd0443eab","3860976cd3d721b01da00872884b6cca"]
API_INDEX = 0

CITIES = ["Delhi", "Mumbai", "Tumakuru", "Chennai", "Sirsi", "Ballari", "Mangaluru", "Mysuru", "Electronic city", "Kolar", "Nelamangala", "Hyderabad"]

def get_api_key():
    global API_INDEX
    key = API_KEYS[API_INDEX]
    API_INDEX = (API_INDEX + 1) % len(API_KEYS)
    return key

def fetch_aqi(city):
    API_KEY = get_api_key()
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url).json()

    if geo_response:
        LAT = geo_response[0]["lat"]
        LON = geo_response[0]["lon"]

        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
        aqi_response = requests.get(aqi_url).json()

        if "list" in aqi_response and len(aqi_response["list"]) > 0:
            aqi = aqi_response["list"][0]["main"]["aqi"]
            components = aqi_response["list"][0]["components"]
            
            return [
                city,
                aqi,
                components.get("pm2_5", "N/A"),
                components.get("pm10", "N/A"),
                components.get("co", "N/A"),
                components.get("no2", "N/A"),
            ]

    return [city, "Error", "N/A", "N/A", "N/A", "N/A"]

# Collect data for all cities
data = [["City", "AQI", "PM2.5", "PM10", "CO", "NO2"]]
for city in CITIES:
    print(f"Fetching data for {city}...")
    data.append(fetch_aqi(city))
    time.sleep(2)  # Delay to avoid API rate limits

# Save data to CSV
with open("aqi_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("\n✅ Data collection complete! Check 'aqi_dataset.csv'")
