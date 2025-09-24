"""Tests for the user repository using an in-memory mongo mock."""

from datetime import datetime

import pytest
from bson import ObjectId
from mongomock import MongoClient

from ..models.user import OAuthProvider, UserCreate
from ..repositories.user_repository import UserRepository


class FakeAsyncCollection:
    """Async wrapper around a synchronous mongomock collection for tests."""

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


@pytest.mark.asyncio
async def test_create_user_inserts_document() -> None:
    repo = get_repository()
    payload = UserCreate(
        provider=OAuthProvider.DISCORD,
        provider_account_id="123",
        username="Tester",
        avatar_url=None,
    )

    user = await repo.create(payload)

    assert user.provider == OAuthProvider.DISCORD
    assert user.provider_account_id == "123"
    assert user.username == "Tester"
    assert user.avatar_url is None
    assert ObjectId.is_valid(user.id)
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


@pytest.mark.asyncio
async def test_get_by_provider_account_returns_user() -> None:
    repo = get_repository()
    payload = UserCreate(
        provider=OAuthProvider.DISCORD,
        provider_account_id="abc",
        username="DiscordUser",
        avatar_url="http://avatar",
    )
    created = await repo.create(payload)

    fetched = await repo.get_by_provider_account(OAuthProvider.DISCORD, "abc")

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.username == "DiscordUser"
    assert fetched.avatar_url == "http://avatar"


@pytest.mark.asyncio
async def test_get_by_provider_account_returns_none_for_unknown() -> None:
    repo = get_repository()

    fetched = await repo.get_by_provider_account(OAuthProvider.DISCORD, "missing")

    assert fetched is None


@pytest.mark.asyncio
async def test_update_login_timestamp_updates_value() -> None:
    repo = get_repository()
    created = await repo.create(
        UserCreate(
            provider=OAuthProvider.DISCORD,
            provider_account_id="id",
            username="name",
            avatar_url=None,
        )
    )

    updated = await repo.update_login_timestamp(created.id)

    assert updated is not None
    assert isinstance(updated.updated_at, datetime)
    assert updated.updated_at >= updated.created_at
