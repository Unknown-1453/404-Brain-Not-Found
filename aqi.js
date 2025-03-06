/*const apiKey = "5841e4968d530deb5e2ce0edbbfc8339"; // Replace with your actual API key
const lat = 12.9756;
const lon = 77.5923;
const url = `http://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=${apiKey}`;

async function getAQIData() {
    try {
        const response = await fetch(url); // No need to import 'fetch' in Node.js 22+
        const data = await response.json();
        console.log("AQI Data:", data);
    } catch (error) {
        console.error("Error fetching AQI data:", error);
    }
}

getAQIData();
*/


/*async function getAQIData() {
    try {
        const response = await fetch(url);
        const data = await response.json();

        console.log("Air Quality Index Data:");
        console.log(`📍 Location: Lat ${data.coord.lat}, Lon ${data.coord.lon}`);

        const airQuality = data.list[0].main.aqi;
        console.log(`🌫 AQI Level: ${airQuality}`);

        console.log("🔬 Pollutants:");
        console.log(data.list[0].components); // Shows all pollutants (PM2.5, CO, NO2, etc.)
    } catch (error) {
        console.error("❌ Error fetching AQI data:", error);
    }
}
*/
const API_KEYS = ["5841e4968d530deb5e2ce0edbbfc8339", "1b1a275ffabba6dbb5ee23f2289bb7ef", "0de7d82479dc3111d395112cd0443eab","3860976cd3d721b01da00872884b6cca"];
let apiIndex = 0; // Keep track of which API key is used

async function getAQIData(city) {
    for (let i = 0; i < API_KEYS.length; i++) {
        const API_KEY = API_KEYS[apiIndex];
        apiIndex = (apiIndex + 1) % API_KEYS.length; // Cycle through keys

        try {
            // Step 1: Get Latitude & Longitude of the City
            let geoResponse = await fetch(`http://api.openweathermap.org/geo/1.0/direct?q=${city}&limit=1&appid=${API_KEY}`);
            let geoData = await geoResponse.json();

            if (geoData.length === 0) {
                console.log("❌ City not found. Trying next API key...");
                continue; // Skip to the next API key
            }

            const { lat, lon } = geoData[0];

            // Step 2: Fetch AQI Data
            let aqiResponse = await fetch(`http://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=${API_KEY}`);
            let aqiData = await aqiResponse.json();

            if (!aqiData.list || aqiData.list.length === 0) {
                console.log("⚠️ Error fetching AQI data. Trying next API key...");
                continue; // Skip to the next API key
            }

            const aqi = aqiData.list[0].main.aqi;
            const components = aqiData.list[0].components;

            const aqiLevels = {
                1: "Good (0-50) 😀",
                2: "Fair (51-100) 🙂",
                3: "Moderate (101-150) 😐",
                4: "Poor (151-200) 😷",
                5: "Very Poor (201-300) 🏭"
            };

            console.log(`\n📍 AQI Report for ${city}`);
            console.log(`AQI Level: ${aqi} - ${aqiLevels[aqi] || "Unknown"}`);
            console.log(`PM2.5: ${components.pm2_5 || "N/A"} µg/m³`);
            console.log(`PM10: ${components.pm10 || "N/A"} µg/m³`);
            console.log(`CO: ${components.co || "N/A"} µg/m³`);
            console.log(`NO₂: ${components.no2 || "N/A"} µg/m³\n`);
            return;
        } catch (error) {
            console.error("❌ Error fetching AQI data. Trying next API key...");
        }
    }

    console.error("❌ All API keys failed. Please check API limits or try again later.");
}

// Get user input (for browser usage, replace with a prompt or input field)
const city = "Delhi"; // Change this to test other cities
getAQIData(city);
