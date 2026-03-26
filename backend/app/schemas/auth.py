"""
Authentication schemas.

What this file does:
- Defines input/output payload contracts for auth endpoints.

Why it is needed:
- Keeps auth API responses stable and explicit for frontend/mobile clients.
"""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """
    Payload for user registration.
    """

    email: EmailStr
    # Bcrypt accepts up to 72 bytes for password input.
    password: str = Field(min_length=8, max_length=72)


class LoginRequest(BaseModel):
    """
    Payload for user login.
    """

    email: EmailStr
    # Keep same limit as register payload for predictable behavior.
    password: str = Field(min_length=8, max_length=72)


class TokenResponse(BaseModel):
    """
    Response payload for successful authentication.
    """

    access_token: str
    token_type: str = "bearer"

