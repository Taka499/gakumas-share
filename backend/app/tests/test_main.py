"""Basic smoke tests for the FastAPI application."""

import pytest
from httpx import ASGITransport, AsyncClient

from ..main import app


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
