import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

def get_llm():

    api_key = os.getenv("OLLAMA_API_KEY")

    # If OLLAMA_API_KEY is present, we run using Ollama Cloud (Remote Host)
    if api_key:
        llm = ChatOllama(
            model="gemma4:31b",
            base_url="https://ollama.com",
            temperature=0,
            client_kwargs={
                "headers": {
                    "Authorization": f"Bearer {api_key}"
                }
            }
        )
    else:
        # Fallback to local Ollama instance
        llm = ChatOllama(
            model="gemma4:31b",
            temperature=0
        )

    return llm

