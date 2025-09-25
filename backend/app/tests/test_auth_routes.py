"""Tests for Discord OAuth routes with patched dependencies."""

import os
from importlib import reload
from typing import Any, Dict

import pytest
from authlib.integrations.base_client.errors import OAuthError
from fastapi.responses import RedirectResponse
from httpx import ASGITransport, AsyncClient
from mongomock import MongoClient

os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017/test")
os.environ.setdefault("MONGODB_DB", "gakumas-share-test")
os.environ.setdefault("DISCORD_CLIENT_ID", "test-client")
os.environ.setdefault("DISCORD_CLIENT_SECRET", "test-secret")
os.environ.setdefault(
    "DISCORD_REDIRECT_URI", "http://localhost:8000/api/auth/discord/callback"
)
os.environ.setdefault("DISCORD_SCOPE", "identify")
os.environ.setdefault("SESSION_SECRET_KEY", "test-session-secret")
os.environ.setdefault("API_BASE_URL", "http://localhost:8000")
os.environ.setdefault("WEB_APP_URL", "http://localhost:5173")
os.environ.setdefault("AUTH_SUCCESS_PATH", "/auth/success")
os.environ.setdefault("AUTH_FAILURE_PATH", "/auth/error")
os.environ.setdefault("SUPERTOKENS_CORE_URL", "http://localhost:3567")

from .. import main

reload(main)

app = main.app

from ..models.user import OAuthProvider  # noqa: E402
from ..repositories.user_repository import UserRepository  # noqa: E402
from ..routers import auth  # noqa: E402


class FakeAsyncCollection:
    """Async wrapper around a mongomock collection for dependency overrides."""

    def __init__(self, collection):
        self._collection = collection

    async def insert_one(self, document):
        return self._collection.insert_one(document)

    async def find_one(self, *args, **kwargs):
        return self._collection.find_one(*args, **kwargs)

    async def find_one_and_update(self, *args, **kwargs):
        return self._collection.find_one_and_update(*args, **kwargs)


def get_repository() -> UserRepository:
    client = MongoClient()
    collection = client["test_db"]["users"]
    return UserRepository(FakeAsyncCollection(collection))


@pytest.fixture(autouse=True)
def cleanup_overrides():
    """Ensure dependency overrides and patches are reset between tests."""

    app.dependency_overrides.pop(auth.get_user_repository, None)
    yield
    app.dependency_overrides.pop(auth.get_user_repository, None)


@pytest.mark.asyncio
async def test_discord_login_redirects_to_discord(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Login endpoint should delegate redirect to Authlib client."""

    captured: Dict[str, Any] = {}

    async def fake_authorize_redirect(request, redirect_uri):
        captured["redirect_uri"] = redirect_uri
        return RedirectResponse(url="https://discord.test/authorize", status_code=303)

    monkeypatch.setattr(
        auth.oauth.discord, "authorize_redirect", fake_authorize_redirect
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/auth/discord/login")

    assert response.status_code == 303
    assert response.headers["location"] == "https://discord.test/authorize"
    assert captured["redirect_uri"] == "http://localhost:8000/api/auth/discord/callback"


@pytest.mark.asyncio
async def test_discord_callback_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Successful callback should upsert user and redirect to success path."""

    async def fake_authorize_access_token(request):  # type: ignore[unused-argument]
        return {"access_token": "token"}

    async def fake_fetch_profile(token: Dict[str, Any]):  # type: ignore[unused-argument]
        return {
            "id": "123",
            "username": "Tester",
            "avatar_url": None,
        }

    async def fake_create_new_session(*args, **kwargs):
        return None

    monkeypatch.setattr(
        auth.oauth.discord,
        "authorize_access_token",
        fake_authorize_access_token,
    )
    monkeypatch.setattr(auth, "_fetch_discord_profile", fake_fetch_profile)
    monkeypatch.setattr(auth, "create_new_session", fake_create_new_session)

    repo = get_repository()
    app.dependency_overrides[auth.get_user_repository] = lambda: repo

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/auth/discord/callback?code=test&state=abc")

    assert response.status_code == 303
    assert (
        response.headers["location"]
        == "http://localhost:5173/auth/success?session=created"
    )

    stored = await repo.get_by_provider_account(OAuthProvider.DISCORD, "123")
    assert stored is not None


@pytest.mark.asyncio
async def test_discord_callback_oauth_error_redirects_to_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OAuth failures should redirect to the configured failure URL."""

    async def fake_authorize_access_token(request):  # type: ignore[unused-argument]
        raise OAuthError("invalid_client")

    monkeypatch.setattr(
        auth.oauth.discord,
        "authorize_access_token",
        fake_authorize_access_token,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/auth/discord/callback?code=test&state=abc")

    assert response.status_code == 303
    assert (
        response.headers["location"]
        == "http://localhost:5173/auth/error?error=oauth_authorisation"
    )
