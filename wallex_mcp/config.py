import os
from datetime import datetime
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Wallex API credentials (optional for public endpoints)
    API_KEY: Optional[str] = Field(None, env=["WALLEX_API_KEY", "wallex_api_key"])
    API_SECRET: Optional[str] = Field(None, env=["WALLEX_API_SECRET", "wallex_api_secret"])
    BASE_URL: str = Field('https://api.wallex.ir', env=["WALLEX_BASE_URL", "wallex_base_url"])

    # Server binding
    HOST: str = Field('0.0.0.0', env='HOST')
    PORT: int = Field(8000, env='PORT')

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    def current_timestamp(self) -> str:
        """Return current UTC timestamp in ISO format."""
        return datetime.utcnow().isoformat()


# Global settings instance
cfg = Settings()
