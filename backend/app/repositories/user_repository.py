"""Data access helpers for the users collection."""

from datetime import datetime
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from ..models.user import OAuthProvider, UserCreate, UserInDB


def _document_to_user(document: dict) -> UserInDB:
    """Convert a MongoDB document into a UserInDB model."""

    return UserInDB(
        id=str(document["_id"]),
        provider=OAuthProvider(document["provider"]),
        provider_account_id=document["provider_account_id"],
        username=document["username"],
        avatar_url=document.get("avatar_url"),
        created_at=document["created_at"],
        updated_at=document["updated_at"],
    )


class UserRepository:
    """Repository encapsulating user persistence logic."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self._collection = collection

    async def create(self, data: UserCreate) -> UserInDB:
        """Insert a new user document and return the stored entity."""

        now = datetime.utcnow()
        document = {
            "provider": data.provider.value,
            "provider_account_id": data.provider_account_id,
            "username": data.username,
            "avatar_url": data.avatar_url,
            "created_at": now,
            "updated_at": now,
        }

        result = await self._collection.insert_one(document)
        document["_id"] = result.inserted_id
        return _document_to_user(document)

    async def get_by_provider_account(
        self, provider: OAuthProvider, provider_account_id: str
    ) -> Optional[UserInDB]:
        """Fetch a user by OAuth provider + account identifier."""

        document = await self._collection.find_one(
            {
                "provider": provider.value,
                "provider_account_id": provider_account_id,
            }
        )
        if document is None:
            return None
        return _document_to_user(document)

    async def get_by_id(self, user_id: str) -> Optional[UserInDB]:
        """Fetch a user by MongoDB ObjectId string."""

        if not ObjectId.is_valid(user_id):
            return None
        document = await self._collection.find_one({"_id": ObjectId(user_id)})
        if document is None:
            return None
        return _document_to_user(document)

    async def update_login_timestamp(self, user_id: str) -> Optional[UserInDB]:
        """Update the user's last login timestamp and return the entity."""

        if not ObjectId.is_valid(user_id):
            return None
        now = datetime.utcnow()
        result = await self._collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": {"updated_at": now}},
            return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return None
        return _document_to_user(result)


__all__ = ["UserRepository"]
