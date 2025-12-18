import requests

MARKET_FORECAST_API_URL = "https://agri-price-forecast.onrender.com/api/predict"

def forecast_price(crop: str, state: str = "Punjab"):
    """
    Fetches crop price forecast and returns standardized AI response.
    
    Args:
        crop: Crop name (e.g., Potato, Onion, Wheat, Tomato, Rice)
        state: State name (e.g., Punjab, Uttar Pradesh, Maharashtra)
    
    Returns:
        Standardized response with type, summary, details, advisory, confidence, source
    """
    params = {"crop": crop, "state": state}
    
    try:
        response = requests.get(
            MARKET_FORECAST_API_URL,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        # Extract price prediction
        predicted_price = data.get("predicted_price", 0)
        
        # Generate advisory based on price
        advisory = []
        if predicted_price > 1500:
            advisory.append(f"Good time to sell {crop}. Prices are favorable.")
            advisory.append("Consider selling in bulk to maximize profits.")
        elif predicted_price > 800:
            advisory.append(f"Moderate prices expected for {crop}.")
            advisory.append("Monitor market trends before selling.")
        else:
            advisory.append(f"Low prices predicted for {crop}.")
            advisory.append("Consider holding stock if storage is available.")
            advisory.append("Explore value-added processing options.")
        
        advisory.append(f"Check local mandi rates in {state} before selling.")
        
        return {
            "type": "market",
            "summary": f"{crop} price forecast: ₹{predicted_price:.2f} per quintal in {state}",
            "details": {
                "crop": crop,
                "state": state,
                "predicted_price": predicted_price,
                "unit": data.get("unit", "₹ per quintal"),
                "horizon": data.get("horizon", "next day")
            },
            "advisory": advisory,
            "confidence": 0.85,
            "source": "ML Price Prediction Model"
        }
        
    except Exception as e:
        return {
            "type": "market",
            "summary": f"Failed to fetch price forecast for {crop} in {state}",
            "details": {"error": str(e), "crop": crop, "state": state},
            "advisory": [
                "Check internet connection",
                "Verify crop and state names",
                "Try again after some time (API may be starting up)"
            ],
            "confidence": 0.0,
            "source": "ML Price Prediction Model"
        }
