import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # LLM Configuration
    OPENAI_MODEL: str = "gpt-4"
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    
    # Application Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FILE_TYPES: list = [".pdf", ".txt"]
    
    # Processing Settings
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.1  # Low temperature for consistent legal analysis
    
    # Risk Classification
    RISK_LEVELS: list = ["Low", "Medium", "High"]
    
    @classmethod
    def validate_api_keys(cls) -> dict:
        """Validate that required API keys are available."""
        status = {
            "openai_available": bool(cls.OPENAI_API_KEY),
            "gemini_available": bool(cls.GEMINI_API_KEY),
            "any_available": bool(cls.OPENAI_API_KEY or cls.GEMINI_API_KEY)
        }
        return status

# Global settings instance
settings = Settings() 