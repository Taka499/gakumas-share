"""OAuth client configuration for external providers."""

from authlib.integrations.starlette_client import OAuth

from .config import Settings

oauth = OAuth()


def configure_oauth(settings: Settings) -> None:
    """Register OAuth providers using application settings."""

    if "discord" in oauth._clients:  # type: ignore[attr-defined]
        return

    oauth.register(
        name="discord",
        client_id=settings.discord_client_id,
        client_secret=settings.discord_client_secret,
        access_token_url="https://discord.com/api/oauth2/token",
        authorize_url="https://discord.com/api/oauth2/authorize",
        api_base_url="https://discord.com/api/",
        client_kwargs={"scope": settings.discord_scope},
    )
