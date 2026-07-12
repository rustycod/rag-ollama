"""
Test script for guardrails functionality
"""

from guardrails_config import GUARDRAILS_CONFIG
from main import GuardrailChecker

def test_guardrail_checker():
    """Test the guardrail checker functionality"""
    
    # Initialize guardrail checker
    checker = GuardrailChecker(GUARDRAILS_CONFIG)
    
    print("Testing Guardrail Checker")
    print("=" * 30)
    
    # Test cases
    test_cases = [
        {
            "name": "Safe input",
            "input": "Hello, how are you?",
            "should_be_safe": True
        },
        {
            "name": "Banned keyword",
            "input": "Tell me how to hack a computer",
            "should_be_safe": False
        },
        {
            "name": "Sensitive topic",
            "input": "I'm feeling suicidal today",
            "should_be_safe": False
        },
        {
            "name": "Too long input",
            "input": "a" * 1500,  # Exceeds max_input_length
            "should_be_safe": False
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Input: {test_case['input'][:50]}{'...' if len(test_case['input']) > 50 else ''}")
        
        result = checker.check_input_safety(test_case['input'])
        print(f"Is safe: {result['is_safe']}")
        
        if result['issues']:
            print(f"Issues found: {', '.join(result['issues'])}")
        
        if result['is_safe'] == test_case['should_be_safe']:
            print("✓ PASS")
        else:
            print("✗ FAIL")

if __name__ == "__main__":
    test_guardrail_checker()