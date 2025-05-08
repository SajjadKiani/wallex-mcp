from datetime import datetime, timezone
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: Optional[str] = Field(
        default=None,
        description="Your Wallex API key (not required for public GET endpoints)",
    )
    base_url: str = Field(
        default="https://api.wallex.ir/v1",
        description="Change only if you are hitting a staging mirror",
    )

    host: str = Field("0.0.0.0", description="IP to bind FastMCP to")
    port: int = Field(8000, description="Port to bind FastMCP to")

    model_config = SettingsConfigDict(
        env_prefix="WALLEX_",            
        env_file=(".env", ".env.local"), 
        env_file_encoding="utf‑8",
        case_sensitive=False,
        extra="ignore",                  
        frozen=True,                     
    )

    @staticmethod
    def utcnow_iso() -> str:
        """Current UTC time in ISO‑8601 with ‘Z’ suffix (RFC‑3339)."""
        return datetime.now(tz=timezone.utc).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        )


cfg = Settings()
