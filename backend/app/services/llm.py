from langchain_ollama import ChatOllama
from app.config import settings

def get_llm(format: str | None = None):
    """Returns a configured instance of the Ollama Chat Model based on settings."""
    kwargs = {
        "base_url": settings.OLLAMA_BASE_URL,
        "model": settings.OLLAMA_MODEL
    }
    if format:
        kwargs["format"] = format
    return ChatOllama(**kwargs)
