import requests
import os

# Use environment variable (no fallback - must be configured)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(location: str = None, lat: float = None, lng: float = None, language: str = "en"):
    """
    Fetches weather data and returns standardized AI response.
    Supports both location name and lat/lng coordinates for accuracy.
    
    Args:
        location: City/location name (optional if lat/lng provided)
        lat: Latitude for precise weather (preferred)
        lng: Longitude for precise weather (preferred)
        language: Language for weather description
    
    Returns:
        Standardized response with type, summary, details, advisory, confidence, source
    """

    try:
        # Use lat/lng if provided for more accurate weather
        if lat is not None and lng is not None:
            params = {
                "lat": lat,
                "lon": lng,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": language
            }
        elif location:
            params = {
                "q": f"{location},IN",
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": language
            }
        else:
            return {
                "type": "weather",
                "summary": "Location not provided",
                "details": {"error": "Either location name or lat/lng coordinates are required"},
                "advisory": ["Please provide your location for weather information"],
                "confidence": 0.0,
                "source": "OpenWeatherMap API"
            }

        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract weather info
        temp = round(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        wind = round(data["wind"]["speed"])
        rain_chance = data.get("clouds", {}).get("all", 0)

        # Generate advisory based on weather
        advisory = []
        if rain_chance > 70:
            advisory.append("High chance of rain. Postpone spraying pesticides.")
            advisory.append("Ensure proper drainage in fields.")
        elif rain_chance > 40:
            advisory.append("Moderate rain expected. Plan irrigation accordingly.")
        
        if temp > 35:
            advisory.append("High temperature. Increase irrigation frequency.")
            advisory.append("Monitor crops for heat stress.")
        elif temp < 10:
            advisory.append("Low temperature. Protect sensitive crops from cold.")
        
        if humidity > 80:
            advisory.append("High humidity. Monitor for fungal diseases.")
        elif humidity < 30:
            advisory.append("Low humidity. Increase irrigation.")
        
        if wind > 20:
            advisory.append("Strong winds. Secure crop covers and structures.")

        if not advisory:
            advisory.append("Weather conditions are favorable for farming activities.")

        # Build standardized response
        return {
            "type": "weather",
            "summary": f"{condition} in {data.get('name')}: {temp}°C, {humidity}% humidity, {description}",
            "details": {
                "location": data.get("name"),
                "temperature": temp,
                "humidity": humidity,
                "condition": condition,
                "description": description,
                "wind_speed": wind,
                "rain_probability": rain_chance
            },
            "advisory": advisory,
            "confidence": 1.0,
            "source": "OpenWeatherMap API"
        }

    except Exception as e:
        return {
            "type": "weather",
            "summary": f"Failed to fetch weather data for {location}",
            "details": {"error": str(e)},
            "advisory": ["Check internet connection and try again"],
            "confidence": 0.0,
            "source": "OpenWeatherMap API"
        }
