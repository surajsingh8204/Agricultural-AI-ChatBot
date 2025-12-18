from chatbot_backend.tools.weather import get_weather
from chatbot_backend.tools.disease import detect_disease
from chatbot_backend.tools.market_forecast import forecast_price
from chatbot_backend.tools.mandi_price import get_mandi_price

def run_tool(intent: str, entities: dict):
    if intent == "weather":
        return get_weather(
            location=entities.get("location"),
            language=entities.get("language", "en")
        )

    if intent == "disease":
        return detect_disease(entities.get("image_url", ""))

    if intent == "market_forecast":
        return forecast_price(
            entities.get("crop", ""),
            entities.get("location", "")
        )

    if intent == "mandi_price":
        return get_mandi_price(
            entities.get("crop", ""),
            entities.get("state", ""),
            entities.get("district", "")
        )

    return None
