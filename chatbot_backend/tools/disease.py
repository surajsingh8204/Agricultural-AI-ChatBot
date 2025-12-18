import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get disease detection API URL from environment, fallback to Render URL
DISEASE_API_URL = os.getenv("DISEASE_DETECTION_API", "https://plant-disease-api-yt7l.onrender.com/predict")

# Disease treatment advisory database
DISEASE_ADVISORY = {
    "healthy": [
        "Your crop appears healthy. Continue current care practices.",
        "Monitor regularly for early signs of disease.",
        "Maintain proper spacing and ventilation."
    ],
    "redrot": [
        "Remove and burn infected canes immediately to prevent spread.",
        "Apply carbendazim or propiconazole fungicide to healthy canes.",
        "Avoid waterlogging and improve field drainage.",
        "Use disease-resistant sugarcane varieties like CoC 671, CoC 92061.",
        "Dip seed sets in Bavistin (0.1%) before planting."
    ],
    "mosaic": [
        "Remove and destroy virus-infected plants.",
        "Control aphid vectors using neem oil or imidacloprid.",
        "Use virus-free, disease-resistant seed material.",
        "Avoid ratoon crop from infected fields."
    ],
    "rust": [
        "Apply sulfur-based fungicide or mancozeb at early infection stage.",
        "Remove infected leaves and dispose properly.",
        "Ensure adequate spacing for air circulation.",
        "Use resistant varieties in future plantings."
    ],
    "yellow": [
        "Improve soil drainage to prevent yellowing.",
        "Apply iron sulfate or zinc sulfate foliar spray.",
        "Check soil pH and adjust if needed (pH 6.0-7.5).",
        "Use balanced fertilization with micronutrients."
    ],
    "blight": [
        "Remove and destroy infected leaves immediately.",
        "Apply copper-based fungicide (Bordeaux mixture).",
        "Avoid overhead irrigation to reduce leaf wetness.",
        "Improve air circulation around plants."
    ],
    "spot": [
        "Prune affected leaves and dispose away from field.",
        "Apply appropriate fungicide (Mancozeb or Chlorothalonil).",
        "Avoid splashing water on leaves during irrigation.",
        "Practice crop rotation next season."
    ],
    "bacterial": [
        "Remove infected plants immediately to prevent spread.",
        "Apply copper-based bactericide.",
        "Disinfect tools between plants.",
        "Improve drainage and avoid waterlogging."
    ],
    "virus": [
        "Remove and destroy infected plants immediately.",
        "Control insect vectors (aphids, whiteflies) with neem oil.",
        "Use virus-free seeds and transplants.",
        "Maintain proper plant nutrition for resilience."
    ],
    "mold": [
        "Improve air circulation around plants.",
        "Reduce humidity through proper spacing.",
        "Apply fungicide (Mancozeb) as preventive measure.",
        "Remove heavily infected leaves."
    ],
    "blast": [
        "Apply Tricyclazole 75% WP or Isoprothiolane 40% EC.",
        "Remove and destroy infected plant parts.",
        "Avoid excessive nitrogen fertilization.",
        "Maintain proper water management in field."
    ],
    "downy": [
        "Apply Metalaxyl + Mancozeb fungicide.",
        "Remove infected leaves showing downy growth.",
        "Reduce humidity and improve air circulation.",
        "Avoid overhead irrigation in evening hours."
    ]
}

def get_advisory_for_disease(disease_name: str):
    """Get treatment advisory based on disease type"""
    disease_lower = disease_name.lower()
    
    # Check for specific disease patterns in normalized form
    # Remove underscores and spaces for better matching
    disease_normalized = disease_lower.replace('_', '').replace(' ', '')
    
    for key, advisory in DISEASE_ADVISORY.items():
        key_normalized = key.replace('_', '').replace(' ', '')
        # Check if the key matches the disease name
        if key_normalized in disease_normalized or disease_normalized in key_normalized:
            return advisory
    
    # Default advisory
    return [
        "Consult local agricultural extension officer for specific treatment.",
        "Send sample to agricultural laboratory for detailed analysis.",
        "Document symptoms with photos for better diagnosis.",
        "Maintain field hygiene and proper crop management."
    ]

def detect_disease(
    image_path: str,
    crop_type: str = "potato"
):
    """
    Detects plant disease from image and returns standardized AI response.
    
    Args:
        image_path: Path to plant/leaf image
        crop_type: potato, tomato, pepper, maize, apple, wheat, rice, mango, sugarcane, finger_millet
    
    Returns:
        Standardized response with type, summary, details, advisory, confidence, source
    """
    try:
        with open(image_path, "rb") as image_file:
            files = {"file": ("image.jpg", image_file, "image/jpeg")}
            data = {"crop": crop_type.lower()}

            response = requests.post(
                DISEASE_API_URL,
                files=files,
                data=data,
                timeout=120  # Increased timeout for Render cold start
            )

            response.raise_for_status()
            result = response.json()
            
            # Extract disease info
            disease_class = result.get("class", "Unknown")
            confidence = result.get("confidence", 0.0)
            
            # Parse disease name (format: Crop___Disease_name)
            disease_parts = disease_class.split("___")
            disease_name = disease_parts[-1].replace("_", " ").title() if len(disease_parts) > 1 else disease_class
            
            # Determine if healthy
            is_healthy = "healthy" in disease_class.lower()
            
            # Get treatment advisory
            advisory = get_advisory_for_disease(disease_class)
            
            # Generate summary
            if is_healthy:
                summary = f"✓ {crop_type.title()} plant is healthy"
            else:
                summary = f"⚠ {disease_name} detected in {crop_type.title()}"
            
            return {
                "type": "disease",
                "class": disease_class,  # For frontend compatibility
                "summary": summary,
                "details": {
                    "crop": crop_type,
                    "disease": disease_name,
                    "full_classification": disease_class,
                    "is_healthy": is_healthy
                },
                "advisory": advisory,
                "confidence": round(confidence, 2),
                "source": "ML Disease Detection Model"
            }
            
    except FileNotFoundError:
        return {
            "type": "disease",
            "summary": f"Image file not found: {image_path}",
            "details": {"error": "File not found", "image_path": image_path},
            "advisory": ["Check image path and try again"],
            "confidence": 0.0,
            "source": "ML Disease Detection Model"
        }
    except Exception as e:
        return {
            "type": "disease",
            "summary": f"Failed to detect disease in {crop_type}",
            "details": {"error": str(e), "crop": crop_type},
            "advisory": [
                "Check image quality (clear, well-lit photo of affected area)",
                "Ensure image shows disease symptoms clearly",
                "Try again after some time (API may be starting up)",
                "Consult local agricultural expert if problem persists"
            ],
            "confidence": 0.0,
            "source": "ML Disease Detection Model"
        }
