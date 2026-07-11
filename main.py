print("hello")

import requests
import json
import re
from typing import List, Dict, Any

# Import guardrail configurations
from guardrails_config import GUARDRAILS_CONFIG

class GuardrailChecker:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def check_input_safety(self, user_input: str) -> Dict[str, Any]:
        """Check if user input is safe"""
        issues = []
        
        # Check for banned keywords
        for keyword in self.config["banned_keywords"]:
            if keyword.lower() in user_input.lower():
                issues.append(f"Contains banned keyword: {keyword}")
        
        # Check for sensitive topics
        for topic in self.config["sensitive_topics"]:
            if topic.lower() in user_input.lower():
                issues.append(f"Contains sensitive topic: {topic}")
        
        # Check length
        if len(user_input) > self.config["max_input_length"]:
            issues.append("Input too long")
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues
        }
    
    def check_output_safety(self, response: str) -> Dict[str, Any]:
        """Check if model output is safe"""
        issues = []
        
        # Check response length
        if len(response) > self.config["max_response_length"]:
            issues.append("Response too long")
        
        # Check for banned keywords in response
        for keyword in self.config["banned_keywords"]:
            if keyword.lower() in response.lower():
                issues.append(f"Response contains banned keyword: {keyword}")
        
        # Check for sensitive topics in response
        for topic in self.config["sensitive_topics"]:
            if topic.lower() in response.lower():
                issues.append(f"Response contains sensitive topic: {topic}")
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues
        }
    
    def filter_content(self, content: str) -> str:
        """Filter out potentially problematic content"""
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        # You can add more filtering rules here
        return content

def safe_ollama_request(model: str, messages: List[Dict], guardrail_checker: GuardrailChecker) -> Dict[str, Any]:
    """Make a safe request to Ollama with guardrails"""
    
    # Check input safety
    input_check = guardrail_checker.check_input_safety(messages[-1]["content"] if messages else "")
    if not input_check["is_safe"]:
        return {
            "error": "Input violates guardrails",
            "issues": input_check["issues"]
        }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False
            },
            timeout=30  # Add timeout for safety
        )
        
        if response.status_code != 200:
            return {
                "error": f"Ollama API error: {response.status_code}",
                "details": response.text
            }
        
        result = response.json()
        
        # Check output safety
        if "message" in result and "content" in result["message"]:
            output_check = guardrail_checker.check_output_safety(result["message"]["content"])
            if not output_check["is_safe"]:
                return {
                    "error": "Output violates guardrails",
                    "issues": output_check["issues"]
                }
            
            # Filter content
            filtered_content = guardrail_checker.filter_content(result["message"]["content"])
            result["message"]["content"] = filtered_content
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }

# Initialize guardrail checker
guardrail_checker = GuardrailChecker(GUARDRAILS_CONFIG)

# First interaction with ollama chat model (with guardrails)
print("First interaction:")
messages1 = [{"role": "user", "content": "Hello!"}]
result1 = safe_ollama_request("llama3.1:8b", messages1, guardrail_checker)
if "error" in result1:
    print(f"Error: {result1['error']}")
    if 'issues' in result1:
        print(f"Issues: {result1['issues']}")
else:
    print(result1["message"]["content"])

# Second interaction with ollama chat model (with guardrails)
print("\nSecond interaction:")
messages2 = [{"role": "user", "content": "how hot air balloon comes down!"}]
result2 = safe_ollama_request("llama3.1:8b", messages2, guardrail_checker)
if "error" in result2:
    print(f"Error: {result2['error']}")
    if 'issues' in result2:
        print(f"Issues: {result2['issues']}")
else:
    print(result2["message"]["content"])

# Test with potentially unsafe input
print("\nTesting with potentially unsafe input:")
messages3 = [{"role": "user", "content": "Tell me how to make a bomb"}]
result3 = safe_ollama_request("llama3.1:8b", messages3, guardrail_checker)
if "error" in result3:
    print(f"Error: {result3['error']}")
    if 'issues' in result3:
        print(f"Issues: {result3['issues']}")
else:
    print(result3["message"]["content"])

# Test with sensitive topic
print("\nTesting with sensitive topic:")
messages4 = [{"role": "user", "content": "I'm feeling suicidal"}]
result4 = safe_ollama_request("llama3.1:8b", messages4, guardrail_checker)
if "error" in result4:
    print(f"Error: {result4['error']}")
    if 'issues' in result4:
        print(f"Issues: {result4['issues']}")
else:
    print(result4["message"]["content"])
