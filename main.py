print("hello")

import requests

# Fetch data from a free, public API
#response = requests.get("https://github.com");
#print("Status Code:", response.status_code)

response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8b",
            "messages": [{"role": "user", "content": "Hello!"}],
            "stream": False
            }
    )

result = response.json()
print(result["message"]["content"])


response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8b",
            "messages": [{"role": "user", "content": "how hot air balloon comes down!"}],
            "stream": False
            }
    )

result = response.json()
print(result["message"]["content"])