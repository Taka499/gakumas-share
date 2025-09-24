"""Application configuration based on environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration values for the backend."""

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mongodb_uri: str = Field(..., alias="MONGODB_URI")
    mongodb_db: str = Field("gakumas-share", alias="MONGODB_DB")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""

    return Settings()

