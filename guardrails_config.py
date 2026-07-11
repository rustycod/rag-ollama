"""
Guardrails Configuration for RAG-Ollama System
"""

# Core guardrail settings
GUARDRAILS_CONFIG = {
    # Response length limits
    "max_response_length": 2000,
    "min_response_length": 1,
    
    # Input validation
    "max_input_length": 1000,
    "max_context_length": 3000,
    
    # Content filtering
    "banned_keywords": [
        "hack", "exploit", "malware", "piracy", "illegal", 
        "violence", "suicide", "self-harm", "weapons", "drugs",
        "adult", "porn", "sex", "bomb", "gun", "knife"
    ],
    
    # Sensitive topics
    "sensitive_topics": [
        "suicide", "self-harm", "violence", "weapons", "drugs",
        "adult", "pornography", "sexual", "hate speech", "discrimination"
    ],
    
    # Allowed domains (for web-based RAG)
    "allowed_domains": [],
    
    # Enable/disable features
    "enable_content_filtering": True,
    "enable_rate_limiting": False,
    "enable_input_validation": True,
    "enable_output_validation": True,
    "log_guardrail_violations": True,
    
    # Timeouts
    "request_timeout": 30,
    "response_timeout": 60,
    
    # Limits
    "max_requests_per_minute": 30
}

# Additional security measures
SECURITY_CONFIG = {
    "enable_cors": False,
    "request_timeout": 30,
    "max_retries": 3,
    "retry_delay": 1,
    "secure_headers": True
}

# Compliance settings
COMPLIANCE_CONFIG = {
    "data_privacy": True,
    "user_consent_required": True,
    "audit_logging": True,
    "data_retention_days": 30
}

# Advanced guardrails for production use
PRODUCTION_GUARDRAILS = {
    **GUARDRAILS_CONFIG,
    "enable_content_filtering": True,
    "enable_rate_limiting": True,
    "enable_input_validation": True,
    "enable_output_validation": True,
    "log_guardrail_violations": True,
    "max_requests_per_minute": 30,
    "response_timeout": 60
}