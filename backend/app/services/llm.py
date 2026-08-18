from langchain_ollama import ChatOllama
from app.config import settings

def get_llm():
    """Returns a configured instance of the Ollama Chat Model based on settings."""
    return ChatOllama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL
    )
