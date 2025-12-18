"""
Offline Retrieval-Based Chatbot System
Uses FAISS vector search for fast semantic similarity matching
Works without internet connection - fallback for when LLM/APIs are unavailable

OPTIMIZATION: Pre-computes and caches embeddings to avoid recalculating on every start
"""

import json
import numpy as np
from typing import List, Dict, Tuple, Optional
import os
import pickle

# Lazy load heavy dependencies
_model = None
_index = None
_data = None
_embeddings = None
_initialized = False

# Data path
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'finaldata_dipsiv.json')
CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'offline_cache.pkl')


def _lazy_init():
    """Lazy initialization of model and index with caching"""
    global _model, _index, _data, _embeddings, _initialized
    
    if _initialized:
        return True
    
    try:
        from sentence_transformers import SentenceTransformer
        import faiss
        
        print("🔄 Initializing Offline Retrieval System...")
        
        # Load model (smaller, faster model for offline use)
        print("  📦 Loading embedding model...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load dataset
        print(f"  📂 Loading dataset from: {DATA_PATH}")
        if not os.path.exists(DATA_PATH):
            print(f"  ⚠️ Dataset not found at: {DATA_PATH}")
            return False
        
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            _data = json.load(f)
        
        print(f"  ✅ Loaded {len(_data)} Q&A pairs")
        
        # Check for cached embeddings
        if os.path.exists(CACHE_PATH):
            print("  📦 Loading cached embeddings...")
            try:
                with open(CACHE_PATH, 'rb') as f:
                    cache = pickle.load(f)
                    if cache.get('data_hash') == len(_data):  # Simple validation
                        _embeddings = cache['embeddings']
                        print(f"  ✅ Loaded cached embeddings ({len(_embeddings)} vectors)")
            except Exception as e:
                print(f"  ⚠️ Cache load failed: {e}")
                _embeddings = None
        
        # Generate embeddings if not cached
        if _embeddings is None:
            print("  🔨 Generating embeddings (this may take a few minutes first time)...")
            questions = [item['question'] for item in _data]
            
            # Encode in batches to show progress and avoid memory issues
            batch_size = 512
            all_embeddings = []
            for i in range(0, len(questions), batch_size):
                batch = questions[i:i+batch_size]
                batch_embeddings = _model.encode(batch, show_progress_bar=False)
                all_embeddings.append(batch_embeddings)
                if (i // batch_size) % 10 == 0:
                    print(f"    Progress: {min(i + batch_size, len(questions))}/{len(questions)}")
            
            _embeddings = np.vstack(all_embeddings).astype('float32')
            
            # Cache embeddings for faster future loading
            print("  💾 Caching embeddings for faster startup...")
            try:
                with open(CACHE_PATH, 'wb') as f:
                    pickle.dump({
                        'embeddings': _embeddings,
                        'data_hash': len(_data)
                    }, f)
                print("  ✅ Embeddings cached!")
            except Exception as e:
                print(f"  ⚠️ Could not cache embeddings: {e}")
        
        _embeddings = _embeddings.astype('float32')
        
        # Build FAISS index
        print("  🔨 Building FAISS index...")
        dimension = _embeddings.shape[1]
        _index = faiss.IndexFlatL2(dimension)
        _index.add(_embeddings)
        
        _initialized = True
        print("  ✅ Offline Retrieval System ready!")
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to initialize offline system: {e}")
        return False


def is_offline_ready() -> bool:
    """Check if offline system is initialized and ready"""
    return _initialized


def get_offline_status() -> Dict:
    """Get status of offline system"""
    return {
        "initialized": _initialized,
        "data_path": DATA_PATH,
        "data_exists": os.path.exists(DATA_PATH),
        "cache_exists": os.path.exists(CACHE_PATH),
        "qa_pairs": len(_data) if _data else 0
    }


def initialize_offline_system() -> Dict:
    """Explicitly initialize the offline system (for pre-warming)"""
    success = _lazy_init()
    status = get_offline_status()
    status["success"] = success
    return status


def search_offline(query: str, top_k: int = 3) -> List[Dict]:
    """
    Search for similar questions in offline database
    
    Args:
        query: User's question
        top_k: Number of results to return
        
    Returns:
        List of matching results with questions, answers, and confidence
    """
    if not _lazy_init():
        return []
    
    try:
        # Encode query
        query_embedding = _model.encode([query]).astype('float32')
        
        # Search in FAISS index
        distances, indices = _index.search(query_embedding, top_k)
        
        # Prepare results
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < 0 or idx >= len(_data):
                continue
            
            # Convert L2 distance to similarity score
            confidence = 1 / (1 + dist)
            
            results.append({
                'question': _data[idx]['question'],
                'answer': _data[idx]['answer'],
                'source': _data[idx].get('source', 'offline_kb'),
                'confidence': float(confidence),
                'distance': float(dist)
            })
        
        return results
        
    except Exception as e:
        print(f"Offline search error: {e}")
        return []


def get_offline_answer(query: str, threshold: float = 0.25) -> Dict:
    """
    Get best answer from offline database
    
    Args:
        query: User's question
        threshold: Minimum confidence threshold
        
    Returns:
        Standardized response dict
    """
    results = search_offline(query, top_k=3)
    
    if not results:
        return {
            "type": "offline",
            "summary": "No answer found in offline knowledge base",
            "details": {"query": query},
            "advisory": ["Try rephrasing your question", "Connect to internet for full AI capabilities"],
            "confidence": 0.0,
            "source": "Offline Knowledge Base",
            "message": "माफ़ करें, मुझे इसका उत्तर नहीं मिला। | Sorry, I couldn't find an answer to your question."
        }
    
    best = results[0]
    
    # Check if confidence is too low
    if best['confidence'] < threshold:
        # Return best match with low confidence warning
        return {
            "type": "offline",
            "summary": f"Partial match found (confidence: {best['confidence']:.0%})",
            "details": {
                "query": query,
                "matched_question": best['question'],
                "confidence": best['confidence']
            },
            "advisory": [
                "This answer may not be exactly what you're looking for",
                "Try rephrasing for better results"
            ],
            "confidence": best['confidence'],
            "source": f"Offline KB - {best['source']}",
            "message": f"मुझे पूरा यकीन नहीं है, लेकिन यह मदद कर सकता है:\n\n{best['answer']}"
        }
    
    # Good match found
    return {
        "type": "offline",
        "summary": f"Answer found with {best['confidence']:.0%} confidence",
        "details": {
            "query": query,
            "matched_question": best['question'],
            "confidence": best['confidence'],
            "top_matches": [
                {"question": r['question'], "confidence": r['confidence']}
                for r in results[:3]
            ]
        },
        "advisory": generate_advisory(query, best['answer']),
        "confidence": best['confidence'],
        "source": f"Offline KB - {best['source']}",
        "message": best['answer']
    }


def generate_advisory(query: str, answer: str) -> List[str]:
    """Generate contextual advisory based on query type"""
    query_lower = query.lower()
    
    advisories = []
    
    if any(word in query_lower for word in ['disease', 'pest', 'रोग', 'कीट']):
        advisories.append("Consult local agricultural officer for severe cases")
        advisories.append("Apply treatment in early morning or evening")
    elif any(word in query_lower for word in ['fertilizer', 'खाद', 'urea']):
        advisories.append("Always follow recommended dosage")
        advisories.append("Apply fertilizer when soil is moist")
    elif any(word in query_lower for word in ['water', 'irrigation', 'सिंचाई', 'पानी']):
        advisories.append("Check soil moisture before irrigating")
        advisories.append("Avoid over-irrigation to prevent root rot")
    elif any(word in query_lower for word in ['seed', 'बीज', 'variety']):
        advisories.append("Use certified seeds from authorized dealers")
        advisories.append("Check seed germination rate before sowing")
    else:
        advisories.append("This information is from our offline knowledge base")
        advisories.append("For latest updates, connect to internet")
    
    return advisories


def handle_conversational(query: str) -> Optional[str]:
    """Handle basic conversational queries (greetings, thanks, etc.)"""
    q = query.lower().strip()
    
    # Greetings
    greetings = ['hello', 'hi', 'hey', 'namaste', 'नमस्ते', 'नमस्कार', 'hii', 'helo']
    if any(q.startswith(g) or q == g for g in greetings):
        return (
            "नमस्ते! 🙏 मैं कृषिमित्र हूं, आपका AI खेती सहायक। "
            "मैं खेती, फसल, मौसम, और सरकारी योजनाओं के बारे में आपकी मदद कर सकता हूं।\n\n"
            "Hello! 🙏 I am KrishiMitra, your AI farming assistant. "
            "I can help you with farming, crops, weather, and government schemes."
        )
    
    # Thanks
    thanks = ['thank', 'thanks', 'धन्यवाद', 'शुक्रिया', 'shukriya']
    if any(t in q for t in thanks):
        return "धन्यवाद! 🙏 खेती में शुभकामनाएं! | Thank you! 🙏 Best wishes for your farming!"
    
    # Goodbye
    byes = ['bye', 'goodbye', 'अलविदा', 'फिर मिलेंगे']
    if any(b in q for b in byes):
        return "अलविदा! 🙏 फिर मिलेंगे! | Goodbye! 🙏 See you again!"
    
    # How are you
    how_are_you = ['how are you', 'कैसे हो', 'kaise ho', 'kaisa hai']
    if any(h in q for h in how_are_you):
        return "मैं ठीक हूं! 😊 आपकी क्या मदद कर सकता हूं? | I'm fine! 😊 How can I help you?"
    
    return None


# Example usage
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing Offline Retrieval System")
    print("="*60 + "\n")
    
    # Test queries
    test_queries = [
        "What is PM-KISAN?",
        "गेहूं की खेती कैसे करें?",
        "How to control aphids in wheat?",
        "Best time to sow rice",
    ]
    
    for query in test_queries:
        print(f"Q: {query}")
        response = get_offline_answer(query)
        print(f"A: {response['message'][:200]}...")
        print(f"Confidence: {response['confidence']:.0%}")
        print("-" * 60 + "\n")
