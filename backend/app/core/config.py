"""
Configuration Management - Pydantic Settings

This module centralizes all configuration for the application.
Values are loaded from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Environment variables are automatically loaded from .env file
    and validated by Pydantic.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Allow extra env vars not defined here
    )
    
    # =========================================================================
    # Backend Settings
    # =========================================================================
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    # =========================================================================
    # Database Settings
    # =========================================================================
    DATABASE_PATH: str = "/app/data/research.db"
    
    # =========================================================================
    # Ollama / LLM Settings
    # =========================================================================
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "gpt-oss:20b"
    
    # OpenAI-compatible API (Ollama provides this)
    LLM_BASE_URL: str = "http://ollama:11434/v1"
    LLM_MODEL: str = "gpt-oss:20b"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 4096
    
    # =========================================================================
    # Research Safeguards
    # =========================================================================
    MAX_ITERATIONS: int = 10
    MAX_RESEARCH_TIME_MINUTES: int = 30
    TOKEN_BUDGET: int = 500_000
    
    # =========================================================================
    # Search Settings
    # =========================================================================
    SEARCH_PROVIDER: str = "duckduckgo"
    TAVILY_API_KEY: str | None = None


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Using lru_cache ensures we only load settings once,
    improving performance across the application.
    
    Returns:
        Settings: Application configuration
    """
    return Settings()


# Export singleton for easy import
settings = get_settings()
