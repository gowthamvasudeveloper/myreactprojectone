"""
Security helpers for authentication.

What this file does:
- Hashes and verifies passwords using bcrypt.
- Creates and decodes JWT access tokens.
- Provides OAuth2 bearer token extraction for FastAPI dependencies.

Why it is needed:
- Keeps cryptography/security concerns in one place.
- Makes auth logic reusable across controllers/services.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.settings import settings
from app.utils.errors import ValidationError

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_PASSWORD_BYTES = 72

# Reads tokens from: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


def hash_password(password: str) -> str:
    """
    Hash a plain password with bcrypt.

    Input:
    - `password`: plain user password.

    Output:
    - Secure hashed password string for DB storage.
    """

    password_bytes = password.encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_PASSWORD_BYTES:
        raise ValidationError(
            "Password is too long for bcrypt. Please use at most 72 bytes (ASCII chars)."
        )

    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Compare a plain password against a stored hash.

    Input:
    - `plain_password`: password from login payload.
    - `password_hash`: hashed password stored in database.

    Output:
    - `True` if they match, else `False`.
    """

    # Guard for bcrypt's 72-byte input limit.
    if len(plain_password.encode("utf-8")) > MAX_BCRYPT_PASSWORD_BYTES:
        return False

    try:
        return pwd_context.verify(plain_password, password_hash)
    except ValueError:
        # Some bcrypt backends raise ValueError for oversized input; treat as non-match.
        return False


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """
    Create a signed JWT access token.

    Input:
    - `subject`: identifier stored in the token (`sub`), usually user ID as string.
    - `expires_minutes`: optional override; defaults to settings.

    Output:
    - Encoded JWT string.
    """

    expire_delta = timedelta(
        minutes=expires_minutes
        if expires_minutes is not None
        else settings.access_token_expire_minutes
    )
    expire_at = datetime.now(tz=timezone.utc) + expire_delta

    payload: dict[str, Any] = {"sub": subject, "exp": expire_at}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Input:
    - `token`: JWT string from Authorization header.

    Output:
    - Decoded token payload.

    Raises:
    - `JWTError` if token is invalid/expired.
    """

    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])

