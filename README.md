# RAG-Ollama with Guardrails

This is a Retrieval-Augmented Generation (RAG) system using Ollama that includes comprehensive guardrails for safety and security.

## Features

- **Input Validation**: Checks user inputs for banned keywords and sensitive topics
- **Output Filtering**: Filters model responses to prevent unsafe content
- **Length Limits**: Enforces maximum response and input length limits
- **Timeout Protection**: Prevents hanging requests
- **Error Handling**: Graceful handling of API errors and exceptions

## Guardrails Implemented

1. **Content Filtering**:
   - Banned keywords detection (hack, exploit, malware, violence, etc.)
   - Sensitive topics prevention (suicide, self-harm, weapons, drugs)
   - Response length limits

2. **Security Measures**:
   - Network timeouts
   - Request validation
   - Error recovery

3. **Compliance**:
   - Data privacy considerations
   - Audit logging capability
   - Rate limiting support

## Usage

```python
# Run the main script
python main.py
```

The system will:
1. Process user queries safely
2. Filter out potentially harmful content
3. Return appropriate error messages for violations
4. Provide clear feedback on guardrail violations

## Configuration

Guardrails are configured in `guardrails_config.py` where you can customize:
- Banned keywords and sensitive topics
- Length limits
- Safety thresholds
- Logging preferences