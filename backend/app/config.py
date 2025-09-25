"""Application configuration based on environment variables."""

from functools import lru_cache
from typing import Optional

from pydantic import AnyHttpUrl, Field
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

    discord_client_id: str = Field(..., alias="DISCORD_CLIENT_ID")
    discord_client_secret: str = Field(..., alias="DISCORD_CLIENT_SECRET")
    discord_redirect_uri: AnyHttpUrl = Field(..., alias="DISCORD_REDIRECT_URI")
    discord_scope: str = Field("identify email", alias="DISCORD_SCOPE")

    session_secret_key: str = Field(..., alias="SESSION_SECRET_KEY")

    api_base_url: AnyHttpUrl = Field("http://localhost:8000", alias="API_BASE_URL")
    web_app_url: AnyHttpUrl = Field("http://localhost:5173", alias="WEB_APP_URL")
    auth_success_path: str = Field("/auth/callback", alias="AUTH_SUCCESS_PATH")
    auth_failure_path: str = Field("/auth/error", alias="AUTH_FAILURE_PATH")

    supertokens_core_url: AnyHttpUrl = Field(..., alias="SUPERTOKENS_CORE_URL")
    supertokens_core_api_key: Optional[str] = Field(
        default=None, alias="SUPERTOKENS_CORE_API_KEY"
    )

    access_token_validity_seconds: int = Field(600, alias="ACCESS_TOKEN_VALIDITY")
    refresh_token_validity_seconds: int = Field(
        30 * 24 * 60 * 60, alias="REFRESH_TOKEN_VALIDITY"
    )

    @property
    def cookie_secure(self) -> bool:
        """Determine whether cookies should be marked as secure."""

        return self.api_base_url.scheme == "https"

    @property
    def success_redirect_url(self) -> str:
        """Return absolute URL for successful authentication redirect."""

        return self._join_url(self.web_app_url, self.auth_success_path)

    @property
    def failure_redirect_url(self) -> str:
        """Return absolute URL for failed authentication redirect."""

        return self._join_url(self.web_app_url, self.auth_failure_path)

    @staticmethod
    def _join_url(base: AnyHttpUrl, path: str) -> str:
        base_str = str(base).rstrip("/")
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{base_str}{path}"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""

    return Settings()
