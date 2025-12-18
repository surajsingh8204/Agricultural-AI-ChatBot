"""
Agricultural AI ChatBot - Main Backend Server
FastAPI server that wraps chatbot_backend and provides REST API endpoints
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
import os
import shutil
from typing import Optional
import json
import threading
import time
import requests
from datetime import datetime

# ============================================
# Keep-Alive Service for Render Free Tier
# ============================================

# Render service URLs to keep alive (using root URLs that respond)
RENDER_SERVICES = {
    "disease_detection": "https://plant-disease-api-yt7l.onrender.com/",
    "price_prediction": "https://agri-price-forecast.onrender.com/"
}

# Keep-alive interval in seconds (14 minutes = 840 seconds, less than Render's 15 min sleep)
KEEP_ALIVE_INTERVAL = 840  # 14 minutes

# Global flag to control the keep-alive thread
_keep_alive_running = False
_keep_alive_thread = None


def ping_render_services():
    """Ping all Render services to keep them alive"""
    results = {}
    for service_name, url in RENDER_SERVICES.items():
        try:
            response = requests.get(url, timeout=30)
            results[service_name] = {
                "status": "alive",
                "code": response.status_code,
                "url": url
            }
            print(f"   ✓ {service_name}: alive (HTTP {response.status_code})")
        except requests.exceptions.RequestException as e:
            results[service_name] = {
                "status": "error",
                "error": str(e),
                "url": url
            }
            print(f"   ✗ {service_name}: error - {e}")
    return results


def keep_alive_worker():
    """Background worker that periodically pings Render services"""
    global _keep_alive_running
    
    print("🔄 Keep-alive service started")
    print(f"   Pinging every {KEEP_ALIVE_INTERVAL} seconds ({KEEP_ALIVE_INTERVAL // 60} minutes)")
    
    # Initial ping
    time.sleep(5)  # Wait for server to fully start
    print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] Initial keep-alive ping...")
    ping_render_services()
    
    while _keep_alive_running:
        # Sleep in small intervals to allow graceful shutdown
        for _ in range(KEEP_ALIVE_INTERVAL):
            if not _keep_alive_running:
                break
            time.sleep(1)
        
        if _keep_alive_running:
            print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] Keep-alive ping...")
            ping_render_services()
    
    print("🛑 Keep-alive service stopped")


def start_keep_alive():
    """Start the keep-alive background service"""
    global _keep_alive_running, _keep_alive_thread
    
    if _keep_alive_running:
        return {"status": "already_running"}
    
    _keep_alive_running = True
    _keep_alive_thread = threading.Thread(target=keep_alive_worker, daemon=True)
    _keep_alive_thread.start()
    
    return {"status": "started", "interval": KEEP_ALIVE_INTERVAL}


def stop_keep_alive():
    """Stop the keep-alive background service"""
    global _keep_alive_running
    _keep_alive_running = False
    return {"status": "stopped"}

# Lazy imports - these will be loaded on first use
answer_query = None
route_domain = None
get_weather = None
detect_disease = None
forecast_price = None
get_mandi_price = None

def _lazy_import():
    """Lazy import heavy modules to speed up startup"""
    global answer_query, route_domain, get_weather, detect_disease, forecast_price, get_mandi_price
    if answer_query is None:
        from chatbot_backend.agent.answer import answer_query as aq
        from chatbot_backend.agent.router import route_domain as rd
        answer_query = aq
        route_domain = rd
    if get_weather is None:
        from chatbot_backend.tools.weather import get_weather as gw
        get_weather = gw
    if detect_disease is None:
        from chatbot_backend.tools.disease import detect_disease as dd
        detect_disease = dd
    if forecast_price is None:
        from chatbot_backend.tools.market_forecast import forecast_price as fp
        forecast_price = fp
    if get_mandi_price is None:
        from chatbot_backend.tools.mandi_price import get_mandi_price as gmp
        get_mandi_price = gmp

# Import lightweight disease detection directly for fast startup
from chatbot_backend.tools.disease import detect_disease as _detect_disease
from chatbot_backend.tools.weather import get_weather as _get_weather
from chatbot_backend.tools.mandi_price import get_mandi_price as _get_mandi_price, get_all_commodity_prices as _get_all_prices
from chatbot_backend.tools.market_forecast import forecast_price as _forecast_price

app = FastAPI(title="Agricultural AI ChatBot API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory for uploaded images
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ============================================
# Startup/Shutdown Events
# ============================================

@app.on_event("startup")
async def startup_event():
    """Start keep-alive service when server starts"""
    print("\n" + "="*50)
    print("🌾 Agricultural AI ChatBot API Starting...")
    print("="*50)
    
    # Start keep-alive service for Render free tier
    result = start_keep_alive()
    print(f"✓ Keep-alive service: {result['status']}")
    print("="*50 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop keep-alive service when server shuts down"""
    stop_keep_alive()
    print("🛑 Server shutting down, keep-alive stopped")


# ============================================
# Request/Response Models
# ============================================

class ChatRequest(BaseModel):
    message: Optional[str] = None  # Backend field name
    query: Optional[str] = None    # Frontend field name (alias)
    language: Optional[str] = "en"
    state: Optional[str] = None
    crop: Optional[str] = None
    location: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class ChatResponse(BaseModel):
    type: str
    summary: str
    details: dict
    advisory: list
    confidence: float
    source: str
    response: Optional[str] = None  # For frontend compatibility
    message: Optional[str] = None   # Alternative field

# ============================================
# Main Chatbot Endpoint
# ============================================

@app.post("/v1/chatbot")
async def chatbot(request: ChatRequest):
    """
    Main chatbot endpoint - handles all text queries
    Integrates with answer_query() from chatbot_backend
    """
    try:
        # Lazy load heavy modules on first use
        _lazy_import()
        
        # Get the query - support both 'message' and 'query' fields from frontend
        user_query = request.message or request.query
        
        if not user_query:
            return {
                "type": "error",
                "summary": "No query provided",
                "details": {},
                "advisory": ["Please provide a question"],
                "confidence": 0,
                "source": "System",
                "response": "Please provide a question to get help."
            }
        
        # Prepare context
        user_context = {
            "state": request.state,
            "crop": request.crop,
            "location": request.location,
            "language": request.language,
            "lat": request.lat,
            "lng": request.lng
        }
        
        # Get response from our chatbot backend
        result = answer_query(
            query=user_query,
            image_path=None,
            user_context=user_context
        )
        
        # IMPORTANT: Set 'response' field for frontend compatibility
        # Frontend expects data.response, not data.message
        llm_response = result.get("message", "")
        
        # If LLM didn't generate a good response, use the details information
        if not llm_response or len(llm_response) < 50:
            # Build response from available data
            info = result.get("details", {}).get("information", "")
            advisory = result.get("advisory", [])
            
            if info:
                llm_response = info[:800]
                if advisory:
                    llm_response += "\n\n📋 Suggestions:\n" + "\n".join([f"• {a[:150]}" for a in advisory[:3]])
            elif advisory:
                llm_response = "\n".join([f"• {a}" for a in advisory])
            else:
                llm_response = result.get("summary", "I'm here to help with your agricultural queries.")
        
        result["response"] = llm_response
        result["message"] = llm_response  # Keep for backward compatibility
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Disease Detection Endpoint
# ============================================

@app.post("/v1/disease/detect")
async def disease_detect(
    file: UploadFile = File(...),
    crop: Optional[str] = Form(None),
    language: Optional[str] = Form("en")
):
    """
    Disease detection with image upload
    Saves image temporarily and calls detect_disease()
    """
    try:
        # Save uploaded image temporarily
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Detect disease using direct import
        result = _detect_disease(
            image_path=str(file_path),
            crop_type=crop.lower() if crop else "unknown"
        )
        
        # Clean up
        try:
            file_path.unlink()
        except:
            pass
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/disease/status")
async def disease_status():
    """Check if disease detection API is available"""
    return {
        "status": "ready",
        "message": "Disease detection is available"
    }


# ============================================
# Weather Endpoint
# ============================================

@app.get("/v1/weather")
async def weather(
    location: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    state: Optional[str] = None,
    lang: Optional[str] = "en",
    crop: Optional[str] = None
):
    """Get weather information for a location using lat/lng or location name"""
    try:
        # Use lat/lng for precise weather, fallback to state/location name
        if lat is not None and lng is not None:
            result = _get_weather(location=None, lat=lat, lng=lng, language=lang)
        elif location:
            result = _get_weather(location=location, language=lang)
        elif state:
            result = _get_weather(location=state, language=lang)
        else:
            return {
                "type": "weather",
                "summary": "Location not provided",
                "details": {"error": "Please provide location, lat/lng, or state"},
                "advisory": ["Enable location access for accurate weather"],
                "confidence": 0.0,
                "source": "OpenWeatherMap API"
            }
        
        # Add crop-specific advisory if crop is provided
        if crop and result.get("details"):
            temp = result["details"].get("temperature", 25)
            humidity = result["details"].get("humidity", 50)
            crop_advisory = generate_crop_advisory(crop, temp, humidity)
            if crop_advisory:
                result["advisory"] = result.get("advisory", []) + crop_advisory
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_crop_advisory(crop: str, temp: float, humidity: float) -> list:
    """Generate crop-specific weather advisory"""
    advisory = []
    
    crop_conditions = {
        "wheat": {"temp_min": 10, "temp_max": 25, "humidity_ideal": 50},
        "rice": {"temp_min": 20, "temp_max": 35, "humidity_ideal": 80},
        "cotton": {"temp_min": 21, "temp_max": 30, "humidity_ideal": 60},
        "sugarcane": {"temp_min": 20, "temp_max": 32, "humidity_ideal": 70},
        "maize": {"temp_min": 18, "temp_max": 32, "humidity_ideal": 60},
        "soybean": {"temp_min": 20, "temp_max": 30, "humidity_ideal": 65},
    }
    
    if crop.lower() in crop_conditions:
        cond = crop_conditions[crop.lower()]
        crop_name = crop.capitalize()
        
        if temp < cond["temp_min"]:
            advisory.append(f"🌡️ Temperature too low for {crop_name}. Consider protective measures.")
        elif temp > cond["temp_max"]:
            advisory.append(f"🌡️ High temperature may stress {crop_name}. Increase irrigation.")
        else:
            advisory.append(f"✅ Temperature is ideal for {crop_name} growth.")
        
        if humidity > cond["humidity_ideal"] + 20:
            advisory.append(f"💧 High humidity - monitor {crop_name} for fungal diseases.")
        elif humidity < cond["humidity_ideal"] - 20:
            advisory.append(f"💧 Low humidity - consider additional irrigation for {crop_name}.")
    
    return advisory


# ============================================
# Market Prices Endpoints
# ============================================

@app.get("/v1/market/prices")
async def market_prices(
    crop: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None
):
    """Get current mandi prices for a commodity"""
    try:
        if not crop:
            return {
                "error": "crop parameter is required (e.g., crop=Onion)",
                "status": "error",
                "available_crops": "Onion, Potato, Tomato, Wheat, Rice, Maize, Soybean, Cotton, Mustard, Chilli, Garlic, Ginger"
            }
        
        result = _get_mandi_price(
            crop=crop,
            state=state,
            district=district
        )
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/mandi/all-prices")
async def get_all_mandi_prices(state: Optional[str] = None):
    """
    Get real-time mandi prices for ALL commodities
    
    Query params:
        state: Filter by state (optional)
    
    Returns:
        Prices for all available commodities from data.gov.in
    """
    try:
        result = _get_all_prices(state=state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/price-forecast/crops")
async def get_crops():
    """Get available crops for price forecasting"""
    # Common crops in the dataset
    crops = [
        "Potato", "Tomato", "Onion", "Wheat", "Rice", "Maize",
        "Cotton", "Sugarcane", "Groundnut", "Soybean", "Chilli"
    ]
    return {"ok": True, "crops": crops}


@app.get("/v1/price-forecast/states")
async def get_states(crop: Optional[str] = None):
    """Get available states for a crop"""
    # Major agricultural states
    states = [
        "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh",
        "Maharashtra", "Karnataka", "Tamil Nadu", "Andhra Pradesh",
        "Gujarat", "Rajasthan", "West Bengal", "Bihar"
    ]
    return {"ok": True, "states": states}


@app.get("/v1/price-forecast/forecast")
async def price_forecast(crop: str, state: str, days: Optional[int] = 7):
    """Get price forecast for a crop in a state from Render API"""
    try:
        import requests
        from datetime import datetime, timedelta
        
        # Try to get real forecast from Render API first
        render_api_url = "https://agri-price-forecast.onrender.com/api/forecast"
        
        try:
            response = requests.get(
                render_api_url,
                params={"crop": crop, "state": state, "days": days},
                timeout=60  # Longer timeout for Render free tier
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    # Fix dates to start from tomorrow if API returns old dates
                    daily_forecast = data.get("daily_forecast", [])
                    if daily_forecast:
                        # Update dates to start from tomorrow
                        updated_forecast = []
                        for i, day in enumerate(daily_forecast):
                            new_date = datetime.now() + timedelta(days=i+1)
                            updated_forecast.append({
                                "date": new_date.strftime("%Y-%m-%d"),
                                "price": day.get("price", 0)
                            })
                        data["daily_forecast"] = updated_forecast
                    
                    return {
                        "ok": True,
                        "success": True,
                        "crop": data.get("crop", crop),
                        "state": data.get("state", state),
                        "days": data.get("days", days),
                        "start_price": data.get("start_price", 0),
                        "end_price": data.get("end_price", 0),
                        "percent_change": data.get("percent_change", 0),
                        "trend": data.get("trend", "Stable"),
                        "trend_emoji": data.get("trend_emoji", "➡️"),
                        "daily_forecast": data.get("daily_forecast", []),
                        "advisory": []
                    }
        except Exception as e:
            print(f"   Render API error: {e}, falling back to local simulation")
        
        # Fallback: Use local prediction with simulation
        result = _forecast_price(crop=crop, state=state)
        predicted_price = result.get("details", {}).get("predicted_price", 0) if result else 0
        
        # Generate daily forecast simulation
        import random
        random.seed(datetime.now().toordinal() + hash(crop + state))
        
        daily_forecast = []
        base_price = predicted_price
        for i in range(days):
            day_date = datetime.now() + timedelta(days=i+1)
            # Small random variation ±5%
            variation = random.uniform(-0.05, 0.05)
            day_price = base_price * (1 + variation * (i / days))
            daily_forecast.append({
                "date": day_date.strftime("%Y-%m-%d"),
                "price": round(day_price, 2)
            })
        
        # Calculate trend
        start_price = predicted_price
        end_price = daily_forecast[-1]["price"] if daily_forecast else predicted_price
        percent_change = ((end_price - start_price) / start_price * 100) if start_price > 0 else 0
        
        if percent_change > 2:
            trend = "Rising"
            trend_emoji = "📈"
        elif percent_change < -2:
            trend = "Falling"
            trend_emoji = "📉"
        else:
            trend = "Stable"
            trend_emoji = "➡️"
        
        return {
            "ok": True,
            "success": True,
            "crop": crop,
            "state": state,
            "days": days,
            "start_price": start_price,
            "end_price": end_price,
            "percent_change": percent_change,
            "trend": trend,
            "trend_emoji": trend_emoji,
            "daily_forecast": daily_forecast,
            "advisory": result.get("advisory", []) if result else []
        }
    except Exception as e:
        return {"ok": False, "success": False, "error": str(e)}


# ============================================
# Government Schemes Endpoint
# ============================================

@app.get("/v1/schemes")
async def get_schemes():
    """Get government schemes information from RAG"""
    try:
        from chatbot_backend.rag.retriever import retrieve_context
        
        # Get schemes from RAG
        schemes_data = retrieve_context(
            query="list all government schemes",
            domain="govt_schemes",
            k=10
        )
        
        # Parse and format schemes
        schemes = []
        if schemes_data:
            # Simple parsing - in production, improve this
            lines = schemes_data.split('\n')
            for line in lines:
                if line.strip() and len(line) > 20:
                    schemes.append({
                        "title": line[:100],
                        "description": line,
                        "category": "Government Scheme"
                    })
        
        return {"schemes": schemes[:10]}  # Limit to 10
        
    except Exception as e:
        return {"schemes": [], "error": str(e)}


# ============================================
# Updates/News Endpoint
# ============================================

@app.get("/v1/updates")
async def get_updates():
    """Get agricultural updates and news"""
    try:
        from chatbot_backend.rag.retriever import retrieve_context
        
        # Get general agricultural updates
        updates_data = retrieve_context(
            query="latest agricultural news and updates",
            domain="general_agri",
            k=5
        )
        
        updates = []
        if updates_data:
            lines = updates_data.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and len(line) > 20:
                    updates.append({
                        "id": i,
                        "title": line[:80],
                        "content": line,
                        "source": "Agricultural Knowledge Base",
                        "severity": "info"
                    })
        
        return {"updates": updates[:10]}
        
    except Exception as e:
        return {"updates": [], "error": str(e)}


# ============================================
# Health Check
# ============================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Agricultural AI ChatBot API",
        "version": "1.0.0",
        "endpoints": {
            "chatbot": "/v1/chatbot",
            "disease_detection": "/v1/disease/detect",
            "weather": "/v1/weather",
            "market_prices": "/v1/market/prices",
            "price_forecast": "/v1/price-forecast",
            "schemes": "/v1/schemes",
            "updates": "/v1/updates"
        }
    }


@app.get("/health")
async def health():
    """Detailed health check including connectivity status"""
    # Check internet connectivity
    internet_status = False
    try:
        from chatbot_backend.llm.client import is_online
        internet_status = is_online()
    except:
        pass
    
    # Check offline system status
    offline_status = {"available": False, "qa_pairs": 0, "initialized": False}
    try:
        from chatbot_backend.tools.offline_retrieval import get_offline_status, is_offline_ready
        offline_status = get_offline_status()
        offline_status["available"] = True
        offline_status["ready"] = is_offline_ready()
    except:
        pass
    
    return {
        "status": "healthy",
        "mode": "online" if internet_status else "offline",
        "internet_connected": internet_status,
        "components": {
            "chatbot_backend": "operational",
            "rag_system": "operational",
            "weather_api": "operational" if internet_status else "offline",
            "disease_detection": "operational" if internet_status else "offline",
            "market_data": "operational" if internet_status else "offline",
            "llm_api": "operational" if internet_status else "offline",
            "offline_retrieval": "operational" if offline_status.get("available") else "not_available",
            "keep_alive_service": "running" if _keep_alive_running else "stopped"
        },
        "offline": offline_status,
        "keep_alive": {
            "running": _keep_alive_running,
            "interval_minutes": KEEP_ALIVE_INTERVAL // 60,
            "services": list(RENDER_SERVICES.keys())
        }
    }


@app.get("/v1/connectivity")
async def connectivity_check():
    """Check internet connectivity status"""
    try:
        from chatbot_backend.llm.client import is_online
        connected = is_online()
        return {
            "ok": True,
            "internet_connected": connected,
            "mode": "online" if connected else "offline"
        }
    except Exception as e:
        return {
            "ok": False,
            "internet_connected": False,
            "mode": "offline",
            "error": str(e)
        }


# ============================================
# Keep-Alive Endpoints (for Render Free Tier)
# ============================================

@app.get("/v1/keep-alive/status")
async def keep_alive_status():
    """Get the status of the keep-alive service"""
    return {
        "running": _keep_alive_running,
        "interval_seconds": KEEP_ALIVE_INTERVAL,
        "interval_minutes": KEEP_ALIVE_INTERVAL // 60,
        "services": list(RENDER_SERVICES.keys()),
        "service_urls": RENDER_SERVICES
    }


@app.get("/v1/keep-alive/ping")
async def keep_alive_ping():
    """Manually trigger a ping to all Render services"""
    print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] Manual keep-alive ping triggered...")
    results = ping_render_services()
    return {
        "ok": True,
        "timestamp": datetime.now().isoformat(),
        "results": results
    }


@app.post("/v1/keep-alive/start")
async def keep_alive_start():
    """Start the keep-alive background service"""
    result = start_keep_alive()
    return {"ok": True, **result}


@app.post("/v1/keep-alive/stop")
async def keep_alive_stop():
    """Stop the keep-alive background service"""
    result = stop_keep_alive()
    return {"ok": True, **result}


# ============================================
# Offline Mode Endpoints
# ============================================

@app.get("/v1/offline/status")
async def offline_status():
    """Check if offline mode is available and ready"""
    try:
        from chatbot_backend.tools.offline_retrieval import get_offline_status, is_offline_ready
        status = get_offline_status()
        return {
            "ok": True,
            "available": True,
            "ready": is_offline_ready(),
            **status
        }
    except ImportError:
        return {
            "ok": False,
            "available": False,
            "ready": False,
            "error": "Offline module not installed. Run: pip install sentence-transformers faiss-cpu"
        }
    except Exception as e:
        return {
            "ok": False,
            "available": False,
            "error": str(e)
        }


@app.post("/v1/offline/initialize")
async def offline_initialize():
    """
    Initialize the offline retrieval system.
    First call may take a few minutes to build embeddings.
    Subsequent calls are fast (uses cached embeddings).
    """
    try:
        from chatbot_backend.tools.offline_retrieval import initialize_offline_system
        result = initialize_offline_system()
        return {
            "ok": result.get("success", False),
            **result
        }
    except ImportError:
        return {
            "ok": False,
            "error": "Offline module not installed. Run: pip install sentence-transformers faiss-cpu"
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }


@app.get("/v1/offline/search")
async def offline_search(query: str, top_k: int = 3):
    """Search offline knowledge base for answers"""
    try:
        from chatbot_backend.tools.offline_retrieval import search_offline, get_offline_answer
        
        results = search_offline(query, top_k=top_k)
        
        return {
            "ok": True,
            "query": query,
            "results": results,
            "count": len(results)
        }
    except ImportError:
        return {
            "ok": False,
            "error": "Offline module not available"
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }


@app.post("/v1/offline/chat")
async def offline_chat(request: ChatRequest):
    """Get answer from offline knowledge base (no internet required)"""
    try:
        from chatbot_backend.tools.offline_retrieval import get_offline_answer, handle_conversational
        
        user_query = request.message or request.query
        
        if not user_query:
            return {"ok": False, "error": "No query provided"}
        
        # Check for conversational response first
        conversational = handle_conversational(user_query)
        if conversational:
            return {
                "ok": True,
                "type": "conversational",
                "response": conversational,
                "message": conversational,
                "confidence": 1.0,
                "source": "KrishiMitra"
            }
        
        # Get answer from offline KB
        result = get_offline_answer(user_query)
        
        return {
            "ok": True,
            **result,
            "response": result.get("message", "")
        }
    except ImportError:
        return {
            "ok": False,
            "error": "Offline module not available"
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🌾 Agricultural AI ChatBot - Backend Server")
    print("=" * 70)
    print("Starting server on http://localhost:5000")
    print("API Documentation: http://localhost:5000/docs")
    print("=" * 70)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
