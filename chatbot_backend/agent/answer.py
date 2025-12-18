"""
Central Query Handler - The BRAIN of Agricultural AI ChatBot

COMPLETE RAG + LLM CHAIN FLOW:
===============================
1. User Query comes in
2. LLaMA-3 extracts intent + entities (STEP 2)
3. Route to appropriate Tools / APIs / RAG (STEP 3-4)
4. LLaMA-3 generates farmer-friendly final explanation (STEP 5)
5. Return structured response

ONLINE/OFFLINE MODE:
====================
- ONLINE: Full RAG + LLM chain with Groq API
- OFFLINE: If internet unavailable, uses FAISS-based retrieval with 7,000+ Q&A pairs

This ensures natural language understanding and natural language generation!
"""

from chatbot_backend.tools.disease import detect_disease
from chatbot_backend.tools.weather import get_weather
from chatbot_backend.tools.market_forecast import forecast_price
from chatbot_backend.tools.mandi_price import get_mandi_price
from chatbot_backend.rag.retriever import retrieve_context
from chatbot_backend.llm.client import call_llm, enhance_response_with_llm, extract_entities_with_llm, is_online, NetworkError
import re
import json

# Offline retrieval for fallback
try:
    from chatbot_backend.tools.offline_retrieval import (
        get_offline_answer, 
        handle_conversational,
        is_offline_ready,
        search_offline,
        initialize_offline_system
    )
    OFFLINE_AVAILABLE = True
except ImportError:
    OFFLINE_AVAILABLE = False
    print("⚠️ Offline retrieval not available")


def extract_location(query: str) -> str:
    """Fallback: Extract location from query using keywords"""
    locations = [
        "delhi", "mumbai", "bangalore", "chennai", "kolkata", "hyderabad",
        "pune", "ahmedabad", "lucknow", "jaipur", "chandigarh", "ludhiana",
        "punjab", "haryana", "uttar pradesh", "maharashtra", "karnataka",
        "tamil nadu", "west bengal", "gujarat", "rajasthan", "bihar"
    ]
    
    query_lower = query.lower()
    for loc in locations:
        if loc in query_lower:
            return loc.title()
    
    return "Delhi"


def extract_crop(query: str) -> str:
    """Fallback: Extract crop name from query using keywords"""
    crops = [
        "potato", "onion", "wheat", "tomato", "rice", "maize", "pepper",
        "apple", "mango", "sugarcane", "cotton", "soybean", "groundnut",
        "mustard", "chickpea", "lentil", "banana", "grape", "orange"
    ]
    
    query_lower = query.lower()
    for crop in crops:
        if crop in query_lower:
            return crop.title()
    
    return None


def extract_state(query: str) -> str:
    """Fallback: Extract state from query using keywords"""
    states = [
        "punjab", "haryana", "uttar pradesh", "maharashtra", "karnataka",
        "tamil nadu", "west bengal", "gujarat", "rajasthan", "bihar",
        "madhya pradesh", "andhra pradesh", "telangana", "kerala"
    ]
    
    query_lower = query.lower()
    for state in states:
        if state in query_lower:
            return state.title()
    
    return "Punjab"


def llm_classify_intent(query: str) -> str:
    """
    STEP 2a: Use LLaMA-3 to classify user intent
    """
    prompt = f"""Classify this agricultural query into ONE category.

Query: "{query}"

Categories:
- weather: Questions about weather, rain, temperature, climate
- disease: Questions about plant diseases, crop problems, leaf issues, pests
- market_forecast: Questions about future crop prices, price predictions
- mandi_price: Questions about current mandi rates, today's prices, wholesale rates
- soil: Questions about soil health, fertilizers, nutrients, pH
- scheme: Questions about government schemes, subsidies, PM-KISAN, PMFBY
- crop_advice: Questions about farming practices, cultivation, irrigation
- general: Any other agricultural questions

Reply with ONLY the category name (one word):"""

    try:
        response = call_llm(prompt)
        intent = response.strip().lower().replace('"', '').replace("'", "")
        
        # Normalize intent
        valid_intents = ["weather", "disease", "market_forecast", "mandi_price", "soil", "scheme", "crop_advice", "general"]
        if intent in valid_intents:
            return intent
        
        # Fuzzy match
        for valid in valid_intents:
            if valid in intent:
                return valid
        
        return "general"
    except:
        return "general"


def llm_extract_entities(query: str) -> dict:
    """
    STEP 2b: Use LLaMA-3 to extract entities from query
    """
    try:
        return extract_entities_with_llm(query)
    except:
        # Fallback to keyword extraction
        return {
            "crop": extract_crop(query),
            "location": extract_location(query),
            "state": extract_state(query),
            "district": None,
            "disease": None
        }


def clean_advisory_text(advisory_list: list) -> list:
    """
    Clean up advisory data - remove raw technical data, JSON, MCQ text, etc.
    Only keep human-readable practical advice.
    """
    cleaned = []
    for item in advisory_list[:5]:
        if not item:
            continue
        text = str(item).strip()
        
        # Skip if it looks like raw data or MCQ text
        skip_patterns = [
            'crop_', 'recommendationengine', 'json', '.csv', 'kg/ha',
            'weather_information', '_02', '_01', 'suitability',
            'temp [', 'rainfall [', 'humidity [', 'answer:', 'mcq',
            'general knowledge', 'reasoning:', 'scheme knowledge',
            'agricultural extension', 'this relates to', 'education',
            'pradhan mantri matru', 'pmmvy', 'pregnant women',
            '2025-12', 'en agricultural', 'question:', 'yojana ('
        ]
        if any(skip in text.lower() for skip in skip_patterns):
            continue
        
        # Skip if too short or looks like technical ID
        if len(text) < 15 or text.count('_') > 2:
            continue
        
        # Skip if it has too many special characters (raw data indicator)
        if text.count('[') > 1 or text.count(']') > 1 or text.count(':') > 3:
            continue
        
        # Truncate long text and clean up
        text = text[:150].strip()
        if text and not text.startswith('{') and not text.startswith('['):
            cleaned.append(text)
    
    # If nothing valid found, return helpful default advisories
    return cleaned if cleaned else [
        "Get soil tested at local Krishi Vigyan Kendra",
        "Follow recommended practices for your region",
        "Call farmer helpline: 1800-180-1551 for guidance"
    ]


def llm_generate_response(query: str, tool_data: dict, entities: dict, language: str = "en") -> str:
    """
    STEP 5: Use LLaMA-3 to generate farmer-friendly final response
    
    Takes the raw tool/API/RAG data and creates a natural, helpful response
    Respects the language preference - English by default
    """
    
    # Determine response language
    if language == "hi":
        lang_instruction = "Respond in Hindi (Devanagari script)."
    elif language in ["te", "mr", "ta", "kn", "pa", "bn"]:
        lang_instruction = f"Respond in simple English with some Hindi words if helpful."
    else:
        lang_instruction = "Respond in clear, simple English only. Do NOT use Hindi or Hinglish."
    
    # Clean up the tool data for the prompt - don't include raw technical data
    summary = tool_data.get('summary', '')
    raw_advisory = tool_data.get('advisory', [])
    source = tool_data.get('source', '')
    details = tool_data.get('details', {})
    
    # CRITICAL: Clean up advisory to remove raw data
    advisory = clean_advisory_text(raw_advisory)
    
    # Extract only meaningful information from details
    clean_info = ""
    if isinstance(details, dict):
        for key, value in details.items():
            if key in ['query', 'information', 'domain']:
                continue  # Skip raw data fields
            if value and isinstance(value, (str, int, float)):
                # Skip technical/raw data
                str_val = str(value)
                if not any(skip in str_val.lower() for skip in ['kg/ha', 'temp [', '_0']):
                    clean_info += f"- {key}: {str_val[:100]}\n"
    
    # Build context for LLM
    prompt = f"""You are KrishiMitra, a helpful agricultural assistant for Indian farmers.

USER QUERY: {query}

FARMER'S CONTEXT:
- Crop: {entities.get('crop', 'Not specified')}
- Location: {entities.get('location', 'Not specified')}
- State: {entities.get('state', 'Not specified')}

KEY INFORMATION:
- Topic: {summary}
- Source: {source}
{clean_info}

KEY POINTS TO COVER:
{chr(10).join(['- ' + str(a)[:150] for a in advisory[:4]] if advisory else ['- Provide helpful farming advice'])}

LANGUAGE INSTRUCTION: {lang_instruction}

TASK: Write a helpful, farmer-friendly response that:
1. Directly answers the farmer's question about "{query}"
2. Provides practical, actionable advice
3. Mentions any relevant warnings or precautions
4. Suggests next steps if appropriate

IMPORTANT RULES:
- Do NOT include raw technical data or JSON
- Do NOT mention "tool data", "API", "RAG", or "database"
- Write naturally as if speaking to a farmer
- Keep response between 100-200 words
- Be warm and helpful

RESPONSE:"""

    try:
        return call_llm(prompt)
    except (NetworkError, Exception) as e:
        print(f"   ⚠️ LLM generation failed: {e}")
        
        # Try offline retrieval first for better response
        if OFFLINE_AVAILABLE:
            try:
                offline_result = get_offline_answer(query)
                if offline_result.get("confidence", 0) > 0.4:
                    return offline_result.get("message", "")
            except:
                pass
        
        # Create a clean fallback response (NOT raw data)
        fallback_parts = []
        
        # Use summary if clean
        if summary and not any(skip in summary.lower() for skip in ['kg/ha', 'temp [', 'rainfall [']):
            fallback_parts.append(summary)
        
        # Add clean advisory only
        clean_advisory = clean_advisory_text(advisory) if advisory else []
        if clean_advisory:
            fallback_parts.append("\n\nसुझाव (Suggestions):")
            for i, adv in enumerate(clean_advisory[:3], 1):
                fallback_parts.append(f"{i}. {adv}")
        
        if fallback_parts:
            return "\n".join(fallback_parts)
        else:
            return """I can help you with your farming question. Here are some general suggestions:

1. Get your soil tested at the nearest Krishi Vigyan Kendra
2. Follow recommended practices for your crop and region
3. Call the farmer helpline 1800-180-1551 for specific guidance

Please ask your question again for more specific advice."""


def answer_query(query: str, image_path: str = None, user_context: dict = None):
    """
    MAIN CHAIN HANDLER - Complete RAG + LLM Pipeline
    
    FLOW:
    =====
    1. Check internet connectivity
    2. If OFFLINE: Use FAISS retrieval with 7,000+ Q&A pairs
    3. If ONLINE: Full RAG + LLM chain
       a. Check for conversational queries (greetings, thanks)
       b. LLaMA-3 classifies intent + extracts entities
       c. Route to appropriate Tool/API/RAG based on intent
       d. Get raw data from tools
       e. LLaMA-3 generates final farmer-friendly explanation
    4. Return structured response
    
    Args:
        query: User's question
        image_path: Optional image path for disease detection
        user_context: Optional context (location, crop, etc.)
    
    Returns:
        Standardized response dict with: type, summary, details, advisory, confidence, source, message
    """
    
    print(f"\n{'='*60}")
    print(f"🌾 KRISHIMITRA CHAIN STARTED")
    print(f"{'='*60}")
    print(f"📝 Query: {query}")
    
    # Initialize context
    context = user_context or {}
    
    # =========================================================
    # STEP 0: Check Internet Connectivity - Online vs Offline Mode
    # =========================================================
    internet_available = is_online()
    
    if internet_available:
        print(f"🌐 MODE: ONLINE (Internet available)")
    else:
        print(f"📴 MODE: OFFLINE (No internet connection)")
        
        # Use offline retrieval system
        if OFFLINE_AVAILABLE:
            # Initialize if not ready
            if not is_offline_ready():
                print("   🔄 Initializing offline system...")
                initialize_offline_system()
            
            # Handle conversational queries first
            conversational_response = handle_conversational(query)
            if conversational_response:
                return {
                    "type": "conversational",
                    "summary": "Greeting",
                    "details": {},
                    "advisory": [],
                    "confidence": 1.0,
                    "source": "KrishiMitra (Offline)",
                    "message": conversational_response,
                    "entities": {},
                    "intent": "greeting",
                    "mode": "offline"
                }
            
            # Get offline answer
            offline_result = get_offline_answer(query)
            offline_result["mode"] = "offline"
            offline_result["entities"] = {}
            offline_result["intent"] = "offline_qa"
            return offline_result
        else:
            return {
                "type": "error",
                "summary": "No internet connection",
                "details": {"error": "Internet is required for this feature"},
                "advisory": ["Please check your internet connection", "Connect to WiFi or mobile data"],
                "confidence": 0.0,
                "source": "KrishiMitra",
                "message": "इंटरनेट कनेक्शन नहीं है। कृपया अपना इंटरनेट कनेक्शन जांचें।\n\nNo internet connection. Please check your internet connection.",
                "entities": {},
                "intent": "error",
                "mode": "offline"
            }
    
    # =========================================================
    # ONLINE MODE - Full RAG + LLM Chain
    # =========================================================
    
    # =========================================================
    # STEP 1: Handle Conversational Queries (Greetings, etc.)
    # =========================================================
    if OFFLINE_AVAILABLE:
        conversational_response = handle_conversational(query)
        if conversational_response:
            print(f"   💬 Conversational response")
            return {
                "type": "conversational",
                "summary": "Greeting",
                "details": {},
                "advisory": [],
                "confidence": 1.0,
                "source": "KrishiMitra",
                "message": conversational_response,
                "entities": {},
                "intent": "greeting",
                "mode": "online"
            }
    
    # =========================================================
    # STEP 2: LLaMA-3 Intent Classification + Entity Extraction
    # =========================================================
    print(f"\n🧠 STEP 2: LLaMA-3 analyzing intent and entities...")
    
    try:
        intent = llm_classify_intent(query)
        entities = llm_extract_entities(query)
    except (NetworkError, Exception) as e:
        print(f"   ⚠️ LLM failed, switching to offline mode: {e}")
        # Fallback to offline retrieval
        if OFFLINE_AVAILABLE:
            offline_result = get_offline_answer(query)
            offline_result["mode"] = "offline_fallback"
            return offline_result
        intent = "general"
        entities = {}
    
    # Merge with user context (user context takes priority)
    entities["crop"] = context.get("crop") or entities.get("crop") or extract_crop(query)
    entities["location"] = context.get("location") or entities.get("location") or extract_location(query)
    entities["state"] = context.get("state") or entities.get("state") or extract_state(query)
    
    print(f"   ➡️ Intent: {intent}")
    print(f"   ➡️ Entities: {entities}")
    
    # =========================================================
    # STEP 3-4: Route to Tools / APIs / RAG
    # =========================================================
    print(f"\n🔧 STEP 3-4: Routing to appropriate tool/API/RAG...")
    
    tool_result = None
    
    # ---------------------------------------------------------
    # 🦠 DISEASE DETECTION
    # ---------------------------------------------------------
    if intent == "disease":
        print(f"   ➡️ Disease Detection Tool")
        
        if not image_path:
            tool_result = {
                "type": "disease",
                "summary": "कृपया पौधे की तस्वीर अपलोड करें (Please upload plant image)",
                "details": {"error": "No image provided", "instructions": "Take a clear photo of the affected leaf"},
                "advisory": [
                    "प्रभावित पत्ती की साफ फोटो लें",
                    "अच्छी रोशनी में फोटो खींचें",
                    "15-20 सेमी दूरी से फोटो लें",
                    "Please upload a clear photo of the affected plant leaf"
                ],
                "confidence": 0.0,
                "source": "ML Disease Detection Model"
            }
        else:
            crop_type = entities.get("crop", "unknown") or "unknown"
            tool_result = detect_disease(image_path, crop_type.lower())
            
            # Enhance with RAG knowledge
            if tool_result.get("confidence", 0) > 0.5:
                disease_name = tool_result.get("details", {}).get("disease", "")
                if disease_name:
                    try:
                        rag_context = retrieve_context(
                            f"treatment for {disease_name} in {crop_type}",
                            domain="pest_disease",
                            k=2
                        )
                        if rag_context:
                            tool_result["rag_knowledge"] = rag_context[:500]
                    except:
                        pass
    
    # ---------------------------------------------------------
    # 🌤️ WEATHER QUERY
    # ---------------------------------------------------------
    elif intent == "weather":
        print(f"   ➡️ Weather API")
        
        location = entities.get("location", context.get("location", "Delhi"))
        lat = context.get("lat")
        lng = context.get("lng")
        
        # Use lat/lng for precise weather if available
        if lat is not None and lng is not None:
            print(f"   📍 Using coordinates: lat={lat}, lng={lng}")
            tool_result = get_weather(location=None, lat=lat, lng=lng)
        else:
            print(f"   📍 Using location name: {location}")
            tool_result = get_weather(location=location)
        
        # Enhance with RAG weather advisory
        try:
            condition = tool_result.get("details", {}).get("condition", "normal")
            rag_context = retrieve_context(
                f"farming activities during {condition} weather",
                domain="weather_advisory",
                k=2
            )
            if rag_context:
                tool_result["rag_knowledge"] = rag_context[:400]
        except:
            pass
    
    # ---------------------------------------------------------
    # 📈 MARKET PRICE FORECAST
    # ---------------------------------------------------------
    elif intent == "market_forecast":
        print(f"   ➡️ Market Forecast API")
        
        crop = entities.get("crop", "Potato")
        state = entities.get("state", "Punjab")
        tool_result = forecast_price(crop, state)
        
        # Enhance with RAG market knowledge
        try:
            rag_context = retrieve_context(
                f"market trends and selling tips for {crop}",
                domain="market_knowledge",
                k=2
            )
            if rag_context:
                tool_result["rag_knowledge"] = rag_context[:400]
        except:
            pass
    
    # ---------------------------------------------------------
    # 🏪 MANDI PRICE
    # ---------------------------------------------------------
    elif intent == "mandi_price":
        print(f"   ➡️ Mandi Price API")
        
        crop = entities.get("crop", "Potato")
        state = entities.get("state", "Punjab")
        tool_result = get_mandi_price(crop, state)
    
    # ---------------------------------------------------------
    # 🌱 SOIL / FERTILIZER
    # ---------------------------------------------------------
    elif intent == "soil":
        print(f"   ➡️ Soil Knowledge RAG")
        
        try:
            # Try soil interpretation first
            rag_context = retrieve_context(query, domain="soil_interpretation", k=3)
            
            if not rag_context or len(rag_context.strip()) < 50:
                rag_context = retrieve_context(query, domain="soil_knowledge", k=3)
            
            if rag_context and rag_context.strip():
                lines = rag_context.split('\n')[:5]
                advisory = [line.strip() for line in lines if line.strip() and len(line) > 20]
                
                tool_result = {
                    "type": "soil",
                    "summary": f"मिट्टी और उर्वरक संबंधी जानकारी",
                    "details": {
                        "query": query,
                        "information": rag_context[:600]
                    },
                    "advisory": advisory if advisory else [
                        "मिट्टी की जांच कराएं",
                        "संतुलित उर्वरक का प्रयोग करें",
                        "जैविक खाद का उपयोग करें"
                    ],
                    "confidence": 0.8,
                    "source": "Agricultural Knowledge Base (RAG)"
                }
            else:
                raise Exception("No RAG context found")
        except:
            tool_result = {
                "type": "soil",
                "summary": "Soil and fertilizer guidance",
                "details": {"query": query},
                "advisory": [
                    "Get soil tested at nearest Krishi Vigyan Kendra",
                    "Apply balanced NPK based on soil test report",
                    "Add organic manure like FYM or compost",
                    "Maintain soil pH between 6.0-7.5"
                ],
                "confidence": 0.6,
                "source": "General Agricultural Guidelines"
            }
    
    # ---------------------------------------------------------
    # 📋 GOVERNMENT SCHEMES
    # ---------------------------------------------------------
    elif intent == "scheme":
        print(f"   ➡️ Government Schemes RAG")
        
        try:
            rag_context = retrieve_context(query, domain="govt_schemes", k=4)
            
            if rag_context and rag_context.strip():
                lines = rag_context.split('\n')
                advisory = [line.strip() for line in lines if line.strip() and len(line) > 20][:5]
                
                tool_result = {
                    "type": "scheme",
                    "summary": "सरकारी योजनाओं की जानकारी",
                    "details": {
                        "query": query,
                        "information": rag_context[:800]
                    },
                    "advisory": advisory,
                    "confidence": 0.85,
                    "source": "Government Schemes Database (RAG)"
                }
            else:
                raise Exception("No schemes found")
        except:
            tool_result = {
                "type": "scheme",
                "summary": "Government schemes information",
                "details": {"query": query},
                "advisory": [
                    "PM-KISAN: ₹6000 annual direct benefit",
                    "PMFBY: Crop insurance scheme",
                    "KCC: Kisan Credit Card for loans",
                    "Visit https://pmkisan.gov.in for registration",
                    "Call 1800-180-1551 for helpline"
                ],
                "confidence": 0.7,
                "source": "Government Agricultural Schemes"
            }
    
    # ---------------------------------------------------------
    # 🌾 CROP ADVICE / GENERAL AGRICULTURE
    # ---------------------------------------------------------
    else:
        print(f"   ➡️ General Agriculture RAG")
        
        domains_to_try = [
            "crop_recommendation",
            "modern_farming",
            "organic_farming",
            "general_agri",
            "historic_practices"
        ]
        
        rag_context = None
        used_domain = None
        
        for domain_name in domains_to_try:
            try:
                rag_context = retrieve_context(query, domain=domain_name, k=3)
                if rag_context and len(rag_context.strip()) > 50:
                    used_domain = domain_name
                    print(f"      ✓ Found in {domain_name}")
                    break
            except:
                continue
        
        if rag_context and rag_context.strip():
            lines = rag_context.split('\n')
            advisory = []
            for line in lines:
                line = line.strip()
                if line and len(line) > 20:
                    advisory.append(line[:200])
                if len(advisory) >= 5:
                    break
            
            tool_result = {
                "type": "crop_advice",
                "summary": f"कृषि संबंधी जानकारी",
                "details": {
                    "query": query,
                    "information": rag_context[:700],
                    "domain": used_domain
                },
                "advisory": advisory if advisory else [
                    "Consult local agricultural extension officer",
                    "Follow recommended practices for your region"
                ],
                "confidence": 0.75,
                "source": "Agricultural Knowledge Base (RAG)"
            }
        else:
            # Fallback: Use LLM directly with no RAG context
            print(f"      ⚠️ No RAG context, using LLM directly")
            
            try:
                direct_llm_response = call_llm(f"""As KrishiMitra agricultural assistant, answer this farmer's question:

Question: {query}

Provide practical, helpful advice in simple language. Include:
1. Direct answer to the question
2. Step-by-step guidance if applicable
3. Any precautions or warnings
4. Suggest contacting Krishi Vigyan Kendra if needed

Keep response under 200 words.""")
            except (NetworkError, Exception) as e:
                print(f"      ⚠️ LLM failed, using offline: {e}")
                if OFFLINE_AVAILABLE:
                    offline_result = get_offline_answer(query)
                    offline_result["mode"] = "offline_fallback"
                    return offline_result
                direct_llm_response = "कृपया अपना प्रश्न दोबारा पूछें। Please ask your question again."
            
            tool_result = {
                "type": "general",
                "summary": "कृषि सहायता",
                "details": {
                    "query": query
                },
                "advisory": [
                    "Visit nearest Krishi Vigyan Kendra for detailed guidance",
                    "Call farmer helpline: 1800-180-1551 (toll-free)",
                    "Use Kisan Suvidha mobile app"
                ],
                "confidence": 0.6,
                "source": "KrishiMitra AI Assistant",
                "message": direct_llm_response  # Pre-set the message from direct LLM call
            }
    
    print(f"   ✓ Tool result obtained")
    
    # =========================================================
    # STEP 5: LLaMA-3 Final Response Generation
    # =========================================================
    print(f"\n💬 STEP 5: LLaMA-3 generating farmer-friendly response...")
    
    # Get language preference from context (default to English)
    language = context.get("language", "en")
    
    # If tool_result already has a good message (from direct LLM call), use it
    if tool_result.get("message"):
        llm_response = tool_result.get("message")
        print(f"   ✓ Using pre-generated response")
    else:
        try:
            llm_response = llm_generate_response(query, tool_result, entities, language)
        except (NetworkError, Exception) as e:
            print(f"   ⚠️ LLM response generation failed: {e}")
            
            # Try offline retrieval first
            if OFFLINE_AVAILABLE:
                offline_result = get_offline_answer(query)
                if offline_result.get("confidence", 0) > 0.3:
                    offline_result["mode"] = "offline_fallback"
                    return offline_result
            
            # Create a clean fallback response (not raw data)
            summary = tool_result.get("summary", "")
            raw_advisory = tool_result.get("advisory", [])
            
            # Use clean_advisory_text to filter out raw data
            advisory = clean_advisory_text(raw_advisory)
            
            fallback_parts = []
            if summary and not any(skip in summary.lower() for skip in ['kg/ha', 'temp [', 'rainfall [']):
                fallback_parts.append(summary)
            if advisory:
                fallback_parts.append("\nसुझाव:")
                for adv in advisory[:3]:
                    fallback_parts.append(f"• {adv}")
            
            llm_response = "\n".join(fallback_parts) if fallback_parts else """I can help you with your farming question. 
            
Please contact your local Krishi Vigyan Kendra or call the farmer helpline 1800-180-1551 for specific guidance."""
    
    print(f"   ✓ Response generated")
    
    # =========================================================
    # FINAL: Combine everything into standardized response
    # =========================================================
    
    # Clean advisory in final response too
    clean_final_advisory = clean_advisory_text(tool_result.get("advisory", []))
    
    final_response = {
        "type": tool_result.get("type", "general"),
        "summary": tool_result.get("summary", ""),
        "details": tool_result.get("details", {}),
        "advisory": clean_final_advisory,  # Use cleaned advisory
        "confidence": tool_result.get("confidence", 0.7),
        "source": tool_result.get("source", "KrishiMitra"),
        "message": llm_response,  # The farmer-friendly LLM-generated response
        "entities": entities,  # Include extracted entities for transparency
        "intent": intent,  # Include detected intent
        "mode": "online"  # Indicate online mode
    }
    
    print(f"\n{'='*60}")
    print(f"✅ CHAIN COMPLETE - Response ready!")
    print(f"{'='*60}\n")
    
    return final_response

