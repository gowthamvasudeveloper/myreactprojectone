"""
Category Pydantic schemas.

What this file does:
- Defines request/response models for categories.

Why it is needed:
- Ensures consistent API payloads and validation for category operations.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """
    Shared fields for category schemas.
    """

    name: str = Field(min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    """
    Payload for creating a category.
    """

    pass


class CategoryUpdate(BaseModel):
    """
    Payload for updating a category.

    Input:
    - name is optional so clients can patch only what they want to change.
    """

    name: str | None = Field(default=None, min_length=1, max_length=100)


class CategoryRead(CategoryBase):
    """
    Public representation of a category.
    """

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

