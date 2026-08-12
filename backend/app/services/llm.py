from langchain_ollama import OllamaLLM
from app.config import settings

def get_llm():
    """Returns a configured instance of the Ollama LLM based on settings."""
    return OllamaLLM(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL
    )
