def route_domain(query: str) -> str:
    q = query.lower()

    if any(word in q for word in ["weather", "rain", "temperature"]) and "forecast" not in q.split("price"):
        return "weather"

    if any(word in q for word in ["disease", "leaf", "spot", "blight", "infection"]):
        return "disease"

    # Check mandi/current price BEFORE market forecast (more specific)
    if any(word in q for word in ["mandi", "apmc", "wholesale", "current price", "today's price", "latest price"]):
        return "mandi_price"

    # Market forecast for future prices
    if any(word in q for word in ["price forecast", "will be", "next month", "future price", "predict"]):
        return "market_forecast"

    if any(word in q for word in ["soil", "ph", "fertilizer", "nutrient"]):
        return "soil_rag"

    return "general_rag"
