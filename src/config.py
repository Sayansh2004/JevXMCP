from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    """Centralized production environment settings with automatic validation."""

    # OpenCode Zen / Jev Settings
    OPENCODE_ZEN_API_KEY: str
    JEV_MODEL_NAME: str = "jev-1.13-free"
    OPENCODE_ZEN_BASE_URL: str = "https://opencode.ai/zen"
    SYNTHESIS_MODEL: str = "gpt-4o-mini"

    
    OPENAI_API_KEY: str

    # Neon PostgreSQL Settings
    NEON_DATABASE_URL: str

    # Security Step-Up Authorization Code
    DELETE_CONFIRMATION_SECRET: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Instantiate single global settings object
settings = Settings()