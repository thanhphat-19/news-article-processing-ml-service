import os
from typing import Optional, Dict, Any
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    ## Database
    MQ_URL: str = ""
    REDIS_URL: str = ""
    RMQ_USER: str = ""
    RMQ_PWD: str = ""
    REDIS_PWD: str = ""

    ## Other
    COMMON_DATA_DIR: str = ""
    OUTPUT_DIR: str = ""
    LOG_LEVEL: str = "INFO"
    PROCESS_PARALLEL_TASKS: bool = False

    ## LLMs
    LLM_PROVIDER:Optional[str] = None  # Options: "ollama", "openai", "anthropic", "cohere", "gemini"
    
    # Ollama
    OLLAMA_HOST: Optional[str] = None
    OLLAMA_MODEL: Optional[str] = None
    
    # OpenAI
    OPENAI_API_KEY: Optional[SecretStr] = None
    OPENAI_MODEL: Optional[str] = None
    
    # Anthropic
    ANTHROPIC_API_KEY: Optional[SecretStr] = None
    ANTHROPIC_MODEL: Optional[str] = None
    
    # Gemini
    GEMINI_API_KEY: Optional[SecretStr] = None
    GEMINI_MODEL: Optional[str] = None
    
    # Cohere
    COHERE_API_KEY: Optional[SecretStr] = None
    COHERE_MODEL: Optional[str] = None
    
    # General LLM settings
    LLM_REQUEST_TIMEOUT: int = 60
    TASK_RETRY_COUNT: int = 3
    TASK_RETRY_BACKOFF: int = 5
    
    def get_celery_broker_url(self) -> str:
        """Return the Celery broker URL"""
        return self.MQ_URL
    
    def get_celery_result_backend(self) -> str:
        """Return the Celery result backend URL"""
        return self.REDIS_URL
    
    def get_model_name(self) -> str:
        """Return the appropriate model name based on the provider"""
        if self.LLM_PROVIDER == "ollama":
            return self.OLLAMA_MODEL
        elif self.LLM_PROVIDER == "openai":
            return self.OPENAI_MODEL
        elif self.LLM_PROVIDER == "anthropic":
            return self.ANTHROPIC_MODEL
        elif self.LLM_PROVIDER == "cohere":
            return self.COHERE_MODEL
        elif self.LLM_PROVIDER == "gemini":
            return self.GEMINI_MODEL
        return self.OLLAMA_MODEL  # Default
    
    def validate_api_keys(self) -> Dict[str, Any]:
        """Validate that appropriate API keys are set for the selected provider"""
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            return {"valid": False, "message": "OpenAI API key is required for OpenAI provider"}
        if self.LLM_PROVIDER == "anthropic" and not self.ANTHROPIC_API_KEY:
            return {"valid": False, "message": "Anthropic API key is required for Anthropic provider"}
        if self.LLM_PROVIDER == "cohere" and not self.COHERE_API_KEY:
            return {"valid": False, "message": "Cohere API key is required for Cohere provider"}
        if self.LLM_PROVIDER == "gemini" and not self.GEMINI_API_KEY:
            return {"valid": False, "message": "Gemini API key is required for Gemini provider"}
        return {"valid": True, "message": ""}

app_settings = AppSettings()
settings = app_settings  # For compatibility with existing code
