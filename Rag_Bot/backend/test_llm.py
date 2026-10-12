import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

response = requests.post(
    "https://ollama.com/api/chat",
    headers={
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gemma4:31b",
        "messages": [
            {"role": "user", "content": "Reply only with: LLM test successful"}
        ],
        "stream": False,
    },
)

print("Status code:", response.status_code)
print("Raw response:")
print(response.text)

data = response.json()

if "message" in data:
    print("LLM answer:", data["message"]["content"])
else:
    print("LLM error:", data)