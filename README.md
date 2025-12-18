# 🌾 KrishiMitra - AI-Powered Agricultural Assistant

![KrishiMitra Banner](https://img.shields.io/badge/KrishiMitra-Agricultural%20AI-green?style=for-the-badge&logo=seedling&logoColor=white)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=flat-square&logo=react)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**KrishiMitra** (कृषिमित्र - "Farmer's Friend") is an AI-powered agricultural chatbot designed to help Indian farmers with:

- 🌡️ Real-time weather updates and advisories
- 🦠 Plant disease detection using ML
- 💰 Live mandi (market) prices for 24+ commodities
- 📈 14-day price forecasting with interactive charts
- 📋 Government schemes information
- 🌱 Farming best practices and crop recommendations
- 🗣️ Multilingual support (English & Hindi)

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [ML Models](#-ml-models)
- [Offline Mode](#-offline-mode)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🤖 Intelligent Chatbot
- **RAG-based responses** using ChromaDB vector store with 7,000+ agricultural Q&A pairs
- **LLM Integration** with Groq API (Llama 3.1 8B) for natural conversations
- **KrishiMitra persona** - friendly, farmer-focused responses in simple language
- **Context-aware** answers based on user's location, crop, and season

### 🌡️ Weather Integration
- Real-time weather data from OpenWeatherMap API
- Location-based forecasts (GPS or manual selection)
- Agricultural advisories based on weather conditions
- Supports all Indian states and districts

### 🦠 Disease Detection
- Upload plant leaf images for instant disease diagnosis
- Powered by TensorFlow/Keras CNN model (10 plant varieties, 38 disease classes)
- Treatment recommendations and prevention tips
- Hosted on Render with automatic keep-alive mechanism

### 💰 Market Prices
- **Real-time mandi prices** for 24+ commodities:
  - Vegetables: Onion, Potato, Tomato, Cabbage, Cauliflower, Brinjal
  - Grains: Wheat, Rice, Maize, Jowar, Bajra
  - Pulses: Gram, Tur, Moong, Urad, Masoor
  - Oilseeds: Groundnut, Mustard, Soybean
  - Cash Crops: Cotton, Sugarcane, Chilli
  - Fruits: Apple, Banana, Mango
- Prices from major mandis across India
- Price trends (📈 Rising, 📉 Falling, 📊 Stable)
- State-wise filtering and comparison

### 📈 Price Forecasting
- **14-day price predictions** using ML models
- Interactive Chart.js line graphs
- Trend analysis and selling recommendations
- Powered by trained prediction models on Render

### 📋 Government Schemes
- Information on PM-KISAN, Fasal Bima Yojana, etc.
- Eligibility criteria and application process
- State-specific scheme information

### 🔄 Offline Mode
- Works without internet using FAISS vector search
- 7,000+ cached Q&A pairs for agricultural queries
- Automatic online/offline mode switching
- Pre-built responses for common questions

### 🌐 Multilingual Support
- Full support for **English** and **Hindi**
- Voice input and text-to-speech output
- Localized date/currency formatting

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Frontend (React + Vite)                        │
│                         http://localhost:5173                            │
├─────────────────────────────────────────────────────────────────────────┤
│  ChatInterface │ WeatherWidget │ DiseaseDetection │ PriceChart │ etc    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ HTTP/REST API
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI + Python)                          │
│                         http://localhost:5000                            │
├─────────────────────────────────────────────────────────────────────────┤
│                              Main Router                                 │
│  /v1/chatbot │ /v1/weather │ /v1/disease │ /v1/market │ /v1/forecast   │
└───────┬─────────────┬──────────────┬──────────────┬─────────────────────┘
        │             │              │              │
        ▼             ▼              ▼              ▼
┌───────────┐  ┌─────────────┐  ┌──────────┐  ┌──────────────┐
│  RAG +    │  │   Weather   │  │  Render  │  │   Mandi      │
│  LLM      │  │   API       │  │  ML API  │  │   Price API  │
│  Chain    │  │             │  │          │  │              │
└─────┬─────┘  └─────────────┘  └──────────┘  └──────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Data Layer                                       │
├──────────────┬──────────────┬──────────────┬───────────────────────────┤
│   ChromaDB   │    FAISS     │  JSON Data   │   External APIs           │
│  (Vectors)   │  (Offline)   │  (RAG Docs)  │  (Groq, Weather, etc)     │
└──────────────┴──────────────┴──────────────┴───────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API framework |
| **Python 3.9+** | Core language |
| **LangChain** | RAG orchestration |
| **ChromaDB** | Vector database |
| **FAISS** | Offline vector search |
| **Groq API** | LLM inference (Llama 3.1) |
| **HuggingFace** | Embeddings (all-MiniLM-L6-v2) |
| **Sentence-Transformers** | Offline embeddings |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **Vite** | Build tool |
| **Chart.js** | Price forecast graphs |
| **Axios** | HTTP client |
| **CSS3** | Styling (dark theme) |

### External Services
| Service | Purpose |
|---------|---------|
| **Groq API** | LLM inference |
| **OpenWeatherMap** | Weather data |
| **Render** | ML model hosting |
| **data.gov.in** | Mandi price data |

---

## 📁 Project Structure

```
Agricultural-AI-ChatBot/
├── 📁 chatbot_backend/                 # FastAPI backend
│   ├── main.py                         # API server & all endpoints
│   ├── 📁 agent/
│   │   ├── answer.py                   # Main RAG + LLM chain
│   │   └── router.py                   # Intent classification
│   ├── 📁 llm/
│   │   └── client.py                   # Groq API client + internet check
│   ├── 📁 rag/
│   │   ├── chunker.py                  # Document chunking
│   │   ├── config.py                   # RAG configuration
│   │   ├── embedder.py                 # Embedding generation
│   │   ├── ingest.py                   # Data ingestion pipeline
│   │   ├── loader.py                   # Document loading
│   │   ├── retriever.py                # Context retrieval
│   │   └── vectorstore.py              # ChromaDB operations
│   ├── 📁 tools/
│   │   ├── weather.py                  # Weather API integration
│   │   ├── disease.py                  # Disease detection (Render API)
│   │   ├── mandi_price.py              # Real-time market prices
│   │   ├── market_forecast.py          # Price predictions
│   │   └── offline_retrieval.py        # FAISS offline mode
│   └── 📁 data/
│       └── finaldata_dipsiv.json       # 7000+ Q&A pairs
│
├── 📁 chatbot-frontend/AGRI-BOT/       # React frontend
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── 📁 src/
│   │   ├── main.jsx                    # Entry point
│   │   ├── App.jsx                     # Main app component
│   │   ├── 📁 components/
│   │   │   ├── ChatInterface.jsx       # Main chat UI
│   │   │   ├── ChatInterface.css
│   │   │   ├── ChatSidebar.jsx         # Conversation history
│   │   │   ├── PriceChart.jsx          # Chart.js price graphs
│   │   │   ├── PriceChart.css
│   │   │   ├── WeatherWidget.jsx       # Weather display
│   │   │   ├── DiseaseDetection.jsx    # Image upload & results
│   │   │   ├── MarketPrices.jsx        # Mandi prices
│   │   │   ├── Header.jsx              # Top navigation
│   │   │   ├── Sidebar.jsx             # Quick actions
│   │   │   └── ...
│   │   ├── 📁 context/
│   │   │   └── LanguageContext.jsx     # i18n provider
│   │   ├── 📁 hooks/
│   │   │   └── useLocation.js          # Geolocation hook
│   │   └── 📁 styles/
│   │       └── *.css
│   └── 📁 public/
│       └── assets/
│
├── 📁 data/rag_data/                   # RAG knowledge base (12 categories)
│   ├── crop_recommendation/            # Crop selection guidance
│   │   └── Crop_recommendation.json
│   ├── general_agri/                   # General agriculture
│   │   └── General_agri.json
│   ├── govt_schemes/                   # Government programs
│   │   └── Govt_schemes.json
│   ├── historic_practices/             # Traditional farming
│   │   └── Historic_practices.json
│   ├── market_knowledge/               # Market information
│   │   └── Market_Knowledge.json
│   ├── modern_farming/                 # Modern techniques
│   │   └── Modern_Farming.json
│   ├── organic_farming/                # Organic methods
│   │   └── Organic_Farming.json
│   ├── pest_disease/                   # Pest management
│   │   └── Pest_disease.json
│   ├── soil_interpretation/            # Soil analysis
│   │   └── Soil_interpretation.json
│   ├── soil_knowledge/                 # Soil science
│   │   └── Soil_Knowledge.json
│   ├── weather_advisory/               # Weather guidance
│   │   └── Weather_advisory.json
│   └── weather_rules/                  # Weather-based rules
│       └── Weather_rules.json
│
├── 📁 Plant-Disease-Detection/         # Disease detection model
│   ├── 📁 backend/
│   │   ├── main.py                     # FastAPI (deployed on Render)
│   │   └── requirements.txt
│   ├── 📁 models/ to models9/          # 10 trained models
│   │   └── *.keras, *.h5
│   ├── 📁 training/
│   │   └── training7.ipynb             # Training notebook
│   └── render.yaml                     # Render deployment config
│
├── 📁 crop-price-prediction/           # Price forecast model
│   ├── app.py                          # FastAPI (deployed on Render)
│   ├── requirements.txt
│   ├── render.yaml
│   ├── 📁 data/
│   │   └── Agriculture_price_dataset.csv
│   ├── 📁 models/                      # Trained models
│   ├── 📁 static/                      # Web UI
│   └── 📁 utils/
│       └── predict.py                  # Prediction logic
│
├── 📁 vector_db/                       # ChromaDB persistent storage
│   └── chroma.sqlite3
│
├── .env                                # Environment variables (create this)
├── .env.example                        # Example environment file
├── requirements.txt                    # Python dependencies
├── test_rag.py                         # RAG system tests
└── README.md                           # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- Conda (recommended) or pip
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Agricultural-AI-ChatBot.git
cd Agricultural-AI-ChatBot
```

### 2. Create Python Environment
```bash
# Using Conda (recommended)
conda create -n agri-llm python=3.10 -y
conda activate agri-llm

# Or using venv
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies
```bash
cd chatbot-frontend/AGRI-BOT
npm install
cd ../..
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# ==============================================
# LLM Configuration (Required)
# ==============================================
GROQ_API_KEY=your_groq_api_key_here

# ==============================================
# Weather API (Required for weather features)
# ==============================================
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key

# ==============================================
# External ML APIs (Hosted on Render - Pre-configured)
# ==============================================
DISEASE_DETECTION_API=https://plant-disease-api-yt7l.onrender.com/predict
PRICE_FORECAST_API=https://agri-price-forecast.onrender.com/api/predict

# ==============================================
# Optional: Market Data API
# ==============================================
DATA_GOV_API_KEY=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b
```

### Getting API Keys

| Service | How to Get | Free Tier |
|---------|------------|-----------|
| **Groq API** | [console.groq.com](https://console.groq.com) | Yes, generous limits |
| **OpenWeatherMap** | [openweathermap.org/api](https://openweathermap.org/api) | 1000 calls/day |
| **data.gov.in** | [data.gov.in](https://data.gov.in) | Unlimited |

---

## 🏃 Running the Application

### Option 1: Run Both Servers

**Terminal 1 - Backend:**
```bash
conda activate agri-llm
cd Agricultural-AI-ChatBot
python -m uvicorn chatbot_backend.main:app --host 0.0.0.0 --port 5000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd Agricultural-AI-ChatBot/chatbot-frontend/AGRI-BOT
npm run dev
```

### Option 2: Quick Start Script (Windows)
```powershell
# Start backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "conda activate agri-llm; python -m uvicorn chatbot_backend.main:app --port 5000 --reload"

# Start frontend  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd chatbot-frontend/AGRI-BOT; npm run dev"
```

### Access the Application
| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:5000 |
| **API Documentation** | http://localhost:5000/docs |
| **Health Check** | http://localhost:5000/health |

---

## 📚 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chatbot` | POST | Main chat endpoint |
| `/v1/weather` | GET | Get weather data |
| `/v1/disease/detect` | POST | Detect plant disease |
| `/v1/market/prices` | GET | Get mandi prices |
| `/v1/mandi/all-prices` | GET | Get all commodity prices |
| `/v1/price-forecast/forecast` | GET | Get price forecast |
| `/v1/schemes` | GET | Get govt schemes |
| `/health` | GET | Health check with status |

### Chat Endpoint

```bash
# Request
POST /v1/chatbot
Content-Type: application/json

{
  "query": "What is the current price of onion in Maharashtra?",
  "language": "en",
  "state": "Maharashtra"
}

# Response
{
  "type": "market",
  "summary": "Today's Onion price: ~₹1234/quintal in Maharashtra",
  "details": {
    "commodity": "Onion",
    "modal_price": 1234,
    "trend": "rising",
    "top_markets": ["Lasalgaon: ₹1303/q", "Mumbai APMC: ₹1297/q"]
  },
  "advisory": ["Prices are RISING! Good time to sell."],
  "confidence": 0.85,
  "source": "Market Trend Data",
  "response": "**Today's Onion Market Price** 🌾...",
  "mode": "online"
}
```

### Weather Endpoint

```bash
# By coordinates (GPS)
GET /v1/weather?lat=28.6139&lng=77.2090

# By state name
GET /v1/weather?state=Delhi

# Response
{
  "type": "weather",
  "summary": "Delhi: 18°C, Clouds",
  "details": {
    "temperature": 18,
    "humidity": 65,
    "description": "overcast clouds",
    "wind_speed": 3.5
  },
  "advisory": ["Good conditions for irrigation"]
}
```

### Disease Detection

```bash
# Request
POST /v1/disease/detect
Content-Type: multipart/form-data

file: <plant_image.jpg>
crop: Tomato

# Response
{
  "disease": "Tomato_Early_blight",
  "confidence": 0.95,
  "treatment": ["Remove infected leaves", "Apply Mancozeb"],
  "prevention": ["Use resistant varieties", "Crop rotation"]
}
```

### Market Prices

```bash
# Single commodity
GET /v1/market/prices?crop=Onion&state=Maharashtra

# All commodities
GET /v1/mandi/all-prices?state=Punjab

# Response includes 24 commodities with prices and trends
```

### Price Forecast

```bash
# Request
GET /v1/price-forecast/forecast?crop=Tomato&state=Rajasthan&days=14

# Response
{
  "crop": "Tomato",
  "state": "Rajasthan",
  "days": 14,
  "start_price": 1344.49,
  "end_price": 1296.47,
  "percent_change": -3.57,
  "trend": "Downward",
  "trend_emoji": "📉",
  "daily_forecast": [
    {"date": "2025-12-19", "price": 1344.49},
    {"date": "2025-12-20", "price": 1343.07},
    ...
  ]
}
```

### Keep-Alive Service

```bash
GET /v1/keep-alive/status    # Check if service is running
GET /v1/keep-alive/ping      # Manually ping Render services
POST /v1/keep-alive/start    # Start keep-alive service
POST /v1/keep-alive/stop     # Stop keep-alive service
```

---

## 🤖 ML Models

### Plant Disease Detection

| Property | Value |
|----------|-------|
| **Architecture** | CNN (Convolutional Neural Network) |
| **Framework** | TensorFlow 2.x / Keras |
| **Input Size** | 256x256 RGB images |
| **Plants Supported** | Potato, Tomato, Pepper Bell, Apple, Cherry, Corn, Grape, Peach, Strawberry |
| **Disease Classes** | 38 categories |
| **Accuracy** | ~95% on validation set |
| **Model Size** | ~50 MB per model |
| **Hosted On** | Render (free tier) |
| **API URL** | https://plant-disease-api-yt7l.onrender.com |

### Price Prediction

| Property | Value |
|----------|-------|
| **Algorithm** | Time Series Forecasting (ARIMA/Prophet hybrid) |
| **Features** | Historical prices, seasonality, weather correlation |
| **Crops** | Potato, Onion, Tomato, Wheat, Rice |
| **States** | All major Indian states |
| **Forecast Horizon** | 1-30 days |
| **Hosted On** | Render (free tier) |
| **API URL** | https://agri-price-forecast.onrender.com |

### Keep-Alive Mechanism

Since Render free tier sleeps after 15 minutes of inactivity:
- Backend automatically pings ML services every **14 minutes**
- Services wake up on first request (~30-60 seconds cold start)
- Status visible in `/health` endpoint

---

## 📴 Offline Mode

KrishiMitra works even without internet connectivity!

### How It Works

1. **Startup Check**: System checks internet by pinging Groq API
2. **Mode Selection**: Automatically switches to offline if no internet
3. **FAISS Search**: Uses local vector index for query matching
4. **Cached Responses**: Returns pre-computed answers for 7,000+ questions

### Offline Capabilities

| Feature | Online | Offline |
|---------|--------|---------|
| General Q&A | ✅ LLM-powered | ✅ Cached answers |
| Weather | ✅ Real-time | ❌ Not available |
| Disease Detection | ✅ ML model | ❌ Not available |
| Mandi Prices | ✅ Real-time | ⚠️ Estimated trends |
| Govt Schemes | ✅ Full details | ✅ Cached info |

### Cache Files

```
chatbot_backend/
├── offline_cache.pkl         # FAISS index + embeddings (~10 MB)
└── data/
    └── finaldata_dipsiv.json # Q&A knowledge base
```

### Initialization

```bash
# Cache is auto-generated on first run
# Or manually initialize:
POST /v1/offline/initialize
```

---

## 🧪 Testing

### Test RAG System
```bash
python test_rag.py
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Chat test
curl -X POST http://localhost:5000/v1/chatbot \
  -H "Content-Type: application/json" \
  -d '{"query": "How to grow wheat?"}'

# Weather test
curl "http://localhost:5000/v1/weather?state=Punjab"

# Market price test
curl "http://localhost:5000/v1/market/prices?crop=Onion&state=Maharashtra"
```

---

## 🚀 Deployment

### Frontend (Vercel/Netlify)
```bash
cd chatbot-frontend/AGRI-BOT
npm run build
# Deploy dist/ folder
```

### Backend (Render/Railway)
```yaml
# render.yaml
services:
  - type: web
    name: krishimitra-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn chatbot_backend.main:app --host 0.0.0.0 --port $PORT
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: ESLint with React rules
- **Commits**: Use conventional commits format

### Areas for Contribution
- [ ] Add more regional languages (Tamil, Telugu, etc.)
- [ ] Implement soil testing integration
- [ ] Add crop calendar feature
- [ ] Improve ML model accuracy
- [ ] Add more government schemes
- [ ] Mobile app development

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## � Team

Meet the amazing team behind KrishiMitra:

| Name | Role | Responsibilities |
|------|------|------------------|
| **Suraj** 👑 | Team Leader | AI/ML Engineer, Backend Developer |
| **Sahil** | Full Stack Developer | Frontend Engineer, Backend Developer |
| **Tarun Kumar** | Database Specialist | Database Engineer, Backend Developer |
| **Pankaj Bhatt** | Data Specialist | Data Engineer |
| **Rawat Shubham Narender** | Domain Expert | Agricultural Domain Expertise |
| **Utkarsh Ojha** | Project Coordinator | Planner, Documentation |

---

## �🙏 Acknowledgments

- **OpenWeatherMap** - Weather data API
- **Groq** - Fast LLM inference
- **HuggingFace** - Embedding models
- **PlantVillage Dataset** - Disease detection training data
- **data.gov.in** - Mandi price data
- **Indian Farming Community** - Inspiration and feedback

---

## 📞 Support

Having issues? Here's how to get help:

1. **Check the FAQ** in the [Wiki](../../wiki)
2. **Search existing** [Issues](../../issues)
3. **Create a new issue** with detailed description
4. **Join our community** discussions

---

## 🗺️ Roadmap

### v2.1 (Current)
- ✅ Real-time mandi prices (24 commodities)
- ✅ Price forecast with charts
- ✅ Keep-alive for Render services
- ✅ Offline mode with FAISS

### v2.2 (Planned)
- [ ] Crop calendar integration
- [ ] Soil testing recommendations
- [ ] WhatsApp integration
- [ ] SMS alerts for price changes

### v3.0 (Future)
- [ ] Mobile app (React Native)
- [ ] Voice-first interface
- [ ] Regional language support (5+ languages)
- [ ] Farmer community features

---

<div align="center">

### 🌾 Made with ❤️ for Indian Farmers 🌾

*"कृषि देश की रीढ़ है"*  
*Agriculture is the backbone of the nation*

---

**[⬆ Back to Top](#-krishimitra---ai-powered-agricultural-assistant)**

</div>
