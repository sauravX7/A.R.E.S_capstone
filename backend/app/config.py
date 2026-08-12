from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

settings = Settings()
