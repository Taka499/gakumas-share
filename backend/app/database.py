"""MongoDB database helpers."""

from collections.abc import AsyncGenerator
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from .config import get_settings

_client: Optional[AsyncIOMotorClient] = None


def get_client() -> AsyncIOMotorClient:
    """Create (or reuse) the Motor client instance."""

    global _client
    if _client is None:
        settings = get_settings()
        _client = AsyncIOMotorClient(settings.mongodb_uri)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    """Return the configured MongoDB database handle."""

    settings = get_settings()
    return get_client()[settings.mongodb_db]


def get_user_collection() -> AsyncIOMotorCollection:
    """Return the users collection handle."""

    return get_database()["users"]


async def close_client() -> None:
    """Dispose the global MongoDB client if it exists."""

    global _client
    if _client is not None:
        _client.close()
        _client = None


async def user_collection_dependency() -> AsyncGenerator[AsyncIOMotorCollection, None]:
    """Yield the users collection for FastAPI dependencies."""

    collection = get_user_collection()
    try:
        yield collection
    finally:
        # Client is cached globally; no per-request cleanup required.
        pass

