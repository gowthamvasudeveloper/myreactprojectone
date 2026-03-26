"""
User Pydantic schemas (request/response shapes).

What this file does:
- Defines Pydantic models used to validate incoming payloads and shape outgoing responses.

Why it is needed:
- Controllers should not return ORM objects directly.
- Schemas act like a contract between backend and frontend/mobile clients.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Shared fields for user schemas.

    Output:
    - Used as a base to keep schema definitions DRY.
    """

    email: EmailStr


class UserCreate(UserBase):
    """
    Payload for registering a new user.

    Input:
    - email: user's email address
    - password: plain password (will be hashed by the service layer)
    """

    # Bcrypt input max is 72 bytes; keep API validation aligned.
    password: str = Field(min_length=8, max_length=72)


class UserRead(UserBase):
    """
    Public representation of a user.

    Output:
    - Never includes password or password_hash.
    """

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

