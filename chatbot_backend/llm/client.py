import os
import socket
from pathlib import Path
from groq import Groq

# Load environment variables from .env file in project root
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass  # dotenv not installed, will use system environment variables

# Get API key from environment (standard GROQ_API_KEY or custom Agri-Bot)
api_key = os.getenv("GROQ_API_KEY") or os.getenv("Agri-Bot")

if not api_key:
    raise ValueError(
        "Groq API key not found. Set GROQ_API_KEY or Agri-Bot environment variable.\n"
        "Get your key from: https://console.groq.com/keys"
    )

client = Groq(api_key=api_key)

MODEL_NAME = "llama-3.1-8b-instant"

# If you want faster & lighter:
# MODEL_NAME = "llama3-8b-8192"


def check_internet_connection(timeout: float = 2.0) -> bool:
    """
    Check if internet connection is available
    Tests connection to Groq API server
    
    Returns:
        True if internet is available, False otherwise
    """
    try:
        # Try to connect to Groq API server
        socket.create_connection(("api.groq.com", 443), timeout=timeout)
        return True
    except (socket.timeout, socket.error, OSError):
        return False


def is_online() -> bool:
    """Check if we can reach the LLM API"""
    return check_internet_connection()


class NetworkError(Exception):
    """Raised when network is unavailable"""
    pass


def call_llm(prompt: str) -> str:
    """
    Calls LLaMA-3 via Groq API
    Used ONLY for planning and explanation
    
    Raises:
        NetworkError: If internet connection is not available
    """
    
    # Check internet first
    if not check_internet_connection():
        raise NetworkError("No internet connection - LLM API unreachable")

    SYSTEM_PROMPT = """You are KrishiMitra, an expert agricultural AI assistant helping Indian farmers.

Your capabilities:
- Weather forecasting and farming advisories
- Crop disease diagnosis and treatment recommendations
- Market price predictions and mandi rates
- Soil health management and fertilizer guidance
- Government scheme information (PM-KISAN, PMFBY, KCC, etc.)
- Crop cultivation best practices and modern farming techniques
- Pest management strategies

Communication style:
- Be empathetic and farmer-friendly
- Use simple, clear language avoiding complex technical jargon
- Provide actionable, practical advice
- Include crop-specific and region-specific recommendations when possible
- Mention relevant government schemes and helplines
- Always prioritize farmer safety and sustainable practices

Context awareness:
- You have access to real-time weather data, market prices, and agricultural knowledge base
- When answering, synthesize information from multiple sources (weather APIs, price databases, RAG knowledge)
- If image provided, analyze crop health and provide detailed disease management steps
- Recommend local agricultural extension services (Krishi Vigyan Kendra) when needed

Important:
- Always give practical, implementable solutions
- Consider Indian farming context (monsoon patterns, regional crops, mandi system)
- Mention precautions and safety measures
- Encourage soil testing and balanced fertilizer use
- Promote organic and sustainable farming practices when appropriate"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()


def enhance_response_with_llm(query: str, tool_data: dict) -> str:
    """
    Use LLM to create farmer-friendly explanation from tool/API/RAG results
    
    Args:
        query: Original user query
        tool_data: Standardized response from tools (type, summary, details, advisory, etc.)
    
    Returns:
        Natural, conversational response with explanations
    """
    
    prompt = f"""User Query: {query}

Available Information:
- Type: {tool_data.get('type')}
- Summary: {tool_data.get('summary')}
- Details: {tool_data.get('details')}
- Advisory Points: {tool_data.get('advisory', [])}
- Confidence: {tool_data.get('confidence')}
- Source: {tool_data.get('source')}

Task: Create a natural, farmer-friendly response that:
1. Directly answers the user's question
2. Explains the key information in simple terms
3. Provides the advisory points as actionable steps
4. Adds relevant context (why this matters for farming)
5. Ends with helpful next steps or contact information if needed

Keep response concise (max 200 words) and practical."""

    return call_llm(prompt)


def extract_entities_with_llm(query: str) -> dict:
    """
    Use LLM to extract structured information from natural language query
    
    Args:
        query: User's natural language query
    
    Returns:
        dict with extracted entities like crop, location, state, disease, etc.
    """
    
    prompt = f"""Extract agricultural entities from this query: "{query}"

Return ONLY a Python dictionary (no explanation) with these keys:
- crop: crop name if mentioned (e.g., wheat, rice, potato) or None
- location: city/village name if mentioned or None  
- state: Indian state name if mentioned or None
- district: district name if mentioned or None
- disease: disease name if mentioned or None
- intent: one of [weather, disease, market_price, soil, general, scheme]

Example: {{"crop": "wheat", "location": "Delhi", "state": "Delhi", "district": None, "disease": None, "intent": "market_price"}}

Query: "{query}"
Dictionary:"""

    response = call_llm(prompt)
    
    try:
        # Try to parse as dict
        import ast
        return ast.literal_eval(response)
    except:
        # Fallback to empty dict
        return {}
