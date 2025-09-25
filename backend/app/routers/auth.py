"""Authentication routes integrating Discord OAuth and SuperTokens."""

from typing import Any, Dict, Optional

from authlib.integrations.base_client.errors import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from supertokens_python.recipe.session.asyncio import create_new_session
from supertokens_python.types import RecipeUserId

from ..config import Settings, get_settings
from ..database import user_collection_dependency
from ..models.user import OAuthProvider, UserCreate
from ..oauth import oauth
from ..repositories.user_repository import UserRepository

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_user_repository(
    collection=Depends(user_collection_dependency),
) -> UserRepository:
    """Dependency that provides a UserRepository instance."""

    return UserRepository(collection)


@router.get("/discord/login")
async def discord_login(request: Request, settings: Settings = Depends(get_settings)):
    """Redirect the user to Discord's OAuth2 authorisation page."""

    try:
        return await oauth.discord.authorize_redirect(
            request, str(settings.discord_redirect_uri)
        )
    except OAuthError as exc:  # pragma: no cover - Authlib handles state internally
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/discord/callback")
async def discord_callback(
    request: Request,
    repo: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
):
    """Handle Discord OAuth callback and create a SuperTokens session."""

    try:
        token = await oauth.discord.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(
            url=f"{settings.failure_redirect_url}?error=oauth_authorisation",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    user_info = await _fetch_discord_profile(token)
    if user_info is None:
        return RedirectResponse(
            url=f"{settings.failure_redirect_url}?error=profile_unavailable",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    user_payload = UserCreate(
        provider=OAuthProvider.DISCORD,
        provider_account_id=user_info["id"],
        username=user_info["username"],
        avatar_url=user_info["avatar_url"],
    )

    user = await repo.upsert_oauth_user(user_payload)
    await repo.update_login_timestamp(user.id)

    response = RedirectResponse(
        url=f"{settings.success_redirect_url}?session=created",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    await create_new_session(
        request,
        tenant_id="public",
        recipe_user_id=RecipeUserId(user.id),
        access_token_payload={
            "provider": OAuthProvider.DISCORD.value,
            "provider_account_id": user.provider_account_id,
            "username": user.username,
        },
        session_data_in_database={"provider": OAuthProvider.DISCORD.value},
    )

    return response


async def _fetch_discord_profile(token: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Fetch user profile information from Discord."""

    resp = await oauth.discord.get("users/@me", token=token)
    if resp.status_code != 200:
        return None
    data = resp.json()
    avatar_hash = data.get("avatar")
    avatar_url: Optional[str] = None
    if avatar_hash:
        ext = "gif" if avatar_hash.startswith("a_") else "png"
        avatar_url = f"https://cdn.discordapp.com/avatars/{data['id']}/{avatar_hash}.{ext}?size=256"
    display_name = data.get("global_name") or data.get("username")
    return {
        "id": data["id"],
        "username": display_name,
        "avatar_url": avatar_url,
    }
