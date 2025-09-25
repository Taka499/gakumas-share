"""Pydantic models for user entities."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OAuthProvider(str, Enum):
    """Supported OAuth providers."""

    DISCORD = "discord"


class UserCreate(BaseModel):
    """Input payload when creating a user from OAuth details."""

    provider: OAuthProvider = Field(..., description="OAuth provider name")
    provider_account_id: str = Field(..., description="Provider-specific user ID")
    username: str = Field(..., description="Display name provided by the OAuth provider")
    avatar_url: Optional[str] = Field(
        None, description="Avatar image URL if available from the provider"
    )


class UserInDB(BaseModel):
    """Representation of a user stored in MongoDB."""

    id: str
    provider: OAuthProvider
    provider_account_id: str
    username: str
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserPublic(BaseModel):
    """Public-facing user information returned to clients."""

    id: str
    username: str
    avatar_url: Optional[str] = None
