"""Basic smoke tests for the FastAPI application."""

import os
from importlib import reload

import pytest
from httpx import ASGITransport, AsyncClient

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


@pytest.mark.asyncio
async def test_root_endpoint() -> None:
    """Ensure the welcome endpoint returns the expected payload."""

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Gakumas Share API"}


@pytest.mark.asyncio
async def test_health_endpoint() -> None:
    """Ensure the health check endpoint responds with ok status."""

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")

    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert "timestamp" in payload
