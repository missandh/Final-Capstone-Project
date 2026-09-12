"""Application configuration loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Practo Domain Agent"
    app_env: str = "development"
    max_tokens: int = 500
    max_autonomy: int = 2
    api_prefix: str = "/api/v1"
    guardrails_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
