from langchain_ollama import OllamaLLM
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Track if Ollama is available
_ollama_available = None

def is_ollama_available():
    """Check if Ollama is available."""
    global _ollama_available
    
    if _ollama_available is not None:
        return _ollama_available
    
    try:
        import httpx
        with httpx.Client(timeout=2) as client:
            response = client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            _ollama_available = response.status_code == 200
    except Exception as e:
        logger.warning(f"Ollama not available: {e}")
        _ollama_available = False
    
    return _ollama_available

def get_llm():
    """Returns a configured instance of the Ollama LLM based on settings."""
    if not is_ollama_available():
        logger.warning("Ollama not available. Using fallback mock LLM.")
        return MockLLM()
    
    return OllamaLLM(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL
    )

class MockLLM:
    """Mock LLM for testing when Ollama is not available."""
    
    def with_structured_output(self, schema):
        """Return a mock structured output wrapper."""
        return MockStructuredLLM(schema)
    
    def invoke(self, prompt):
        """Mock invoke - returns a simple response."""
        return f"Mock response to: {prompt[:50]}..."

class MockStructuredLLM:
    """Mock structured LLM for testing."""
    
    def __init__(self, schema):
        self.schema = schema
    
    def invoke(self, prompt):
        """Return a mock structured response based on the schema."""
        # Try to create a mock instance of the schema
        try:
            # For RoutingDecision, return a mock instance
            if hasattr(self.schema, '__name__') and 'Routing' in self.schema.__name__:
                from app.models.routing import RoutingDecision
                return RoutingDecision(next_agent="END", reason="Mock response - Ollama not available")
            
            # Generic fallback
            return self.schema()
        except Exception as e:
            logger.error(f"Failed to create mock response: {e}")
            return None
