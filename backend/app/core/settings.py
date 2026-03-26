"""
Centralized application configuration (settings).

What this file does:
- Defines strongly-typed settings using `pydantic-settings`.
- Loads configuration from environment variables (and optionally from a `.env` file).

Why it is needed:
- Production apps should not hardcode secrets or environment-specific values.
- A typed settings object gives you validation and autocomplete across the codebase.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Inputs:
    - Environment variables (and optionally `.env` in local development).

    Outputs:
    - A validated Settings object used across the backend.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unknown env vars (helps in container environments)
    )

    # App
    app_name: str = Field(default="Expense Manager API", alias="APP_NAME")
    environment: str = Field(default="local", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # API
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        alias="CORS_ORIGINS",
    )

    # Security (JWT)
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Database
    database_url: str = Field(..., alias="DATABASE_URL")


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    Why cache?
    - Settings are read-only configuration.
    - Caching avoids re-reading env vars repeatedly.
    """

    return Settings()


# Convenient singleton-style access for most modules.
settings = get_settings()

