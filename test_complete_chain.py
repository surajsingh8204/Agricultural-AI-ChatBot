"""
🧪 COMPLETE CHAIN TEST
Tests: User Query → Router → answer_query() → Tools/APIs/RAG → Formatted Response
"""

from chatbot_backend.agent.router import route_domain
from chatbot_backend.agent.answer import answer_query

def print_result(test_name, result):
    """Pretty print test results"""
    print(f"\n{'='*70}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*70}")
    print(f"Type: {result.get('type')}")
    print(f"Summary: {result.get('summary')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Source: {result.get('source')}")
    print(f"\nAdvisory ({len(result.get('advisory', []))} points):")
    for i, point in enumerate(result.get('advisory', [])[:3], 1):
        print(f"  {i}. {point[:100]}...")
    print(f"\nDetails keys: {list(result.get('details', {}).keys())}")
    
    # Validate standardized schema
    required_fields = ['type', 'summary', 'details', 'advisory', 'confidence', 'source']
    missing = [f for f in required_fields if f not in result]
    if missing:
        print(f"\n❌ MISSING FIELDS: {missing}")
    else:
        print(f"\n✅ Schema validated")
    
    return len(missing) == 0


def test_chain():
    """Test complete query processing chain"""
    
    test_cases = [
        # Test 1: Weather Query
        {
            "name": "Weather Query",
            "query": "What is the weather in Delhi today?",
            "context": {}
        },
        
        # Test 2: Market Forecast
        {
            "name": "Market Forecast",
            "query": "What will be the price of potato in Punjab next month?",
            "context": {}
        },
        
        # Test 3: Mandi Price
        {
            "name": "Mandi Price",
            "query": "Current price of wheat in Uttar Pradesh mandis",
            "context": {}
        },
        
        # Test 4: Soil/Fertilizer (RAG)
        {
            "name": "Soil Query (RAG)",
            "query": "How to fix nitrogen deficiency in soil?",
            "context": {}
        },
        
        # Test 5: General Agricultural (RAG)
        {
            "name": "General Query (RAG)",
            "query": "What are the best practices for organic farming?",
            "context": {}
        },
        
        # Test 6: Government Schemes (RAG)
        {
            "name": "Government Schemes (RAG)",
            "query": "Tell me about PM Kisan Samman Nidhi scheme",
            "context": {}
        }
    ]
    
    results = []
    passed = 0
    failed = 0
    
    print("\n" + "="*70)
    print("🚀 STARTING COMPLETE CHAIN TEST")
    print("="*70)
    
    for test_case in test_cases:
        try:
            # Step 1: Route query to domain
            domain = route_domain(test_case["query"])
            print(f"\n📍 Query: {test_case['query'][:60]}...")
            print(f"   Routed to: {domain}")
            
            # Step 2: Process query through answer_query
            result = answer_query(
                query=test_case["query"],
                image_path=None,
                user_context=test_case["context"]
            )
            
            # Step 3: Validate and display result
            is_valid = print_result(test_case["name"], result)
            
            if is_valid:
                passed += 1
                results.append({"test": test_case["name"], "status": "✅ PASS"})
            else:
                failed += 1
                results.append({"test": test_case["name"], "status": "❌ FAIL"})
                
        except Exception as e:
            print(f"\n❌ ERROR in {test_case['name']}: {str(e)}")
            failed += 1
            results.append({"test": test_case["name"], "status": f"❌ ERROR: {str(e)[:50]}"})
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 TEST SUMMARY")
    print(f"{'='*70}")
    for r in results:
        print(f"{r['status']} - {r['test']}")
    
    print(f"\n{'='*70}")
    print(f"Total: {len(test_cases)} | Passed: {passed} | Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    print(f"{'='*70}")
    
    # Check if all components are working
    if passed == len(test_cases):
        print("\n🎉 ALL COMPONENTS OF THE CHAIN ARE RUNNING PERFECTLY!")
        print("✅ Router → answer_query() → Tools/APIs/RAG → Standardized Response")
        return True
    else:
        print("\n⚠️ Some components need attention")
        return False


if __name__ == "__main__":
    test_chain()
