"""
Reusable FastAPI dependencies.

What this file does:
- Provides dependency helpers shared across endpoints.
- Includes `get_current_user` for JWT-protected routes.

Why it is needed:
- Avoids repeating token decode/user lookup logic in each controller.
"""

from __future__ import annotations

from fastapi import Depends
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, oauth2_scheme
from app.db.session import get_db
from app.models import User
from app.repositories.user_repository import UserRepository
from app.utils.errors import UnauthorizedError


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the currently authenticated user from a bearer token.

    Inputs:
    - `token`: JWT from Authorization header.
    - `db`: request-scoped database session.

    Output:
    - Authenticated `User` entity.

    Raises:
    - `UnauthorizedError` when token is invalid/expired or user does not exist.
    """

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise UnauthorizedError("Invalid authentication token.")
        user_id = int(subject)
    except (JWTError, ValueError):
        raise UnauthorizedError("Invalid or expired authentication token.") from None

    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)
    if not user:
        raise UnauthorizedError("Authenticated user no longer exists.")

    return user

