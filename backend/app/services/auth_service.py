"""
Authentication service (business logic layer).

What this file does:
- Handles registration and login rules.
- Validates credentials.
- Builds JWT access tokens.

Why it is needed:
- Keeps business/auth logic out of controllers.
- Enables easier unit testing compared to route-bound code.
"""

from __future__ import annotations

from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.repositories.user_repository import UserRepository
from app.utils.errors import ConflictError, UnauthorizedError


class AuthService:
    """
    Auth business logic.

    Input:
    - `user_repository`: abstraction for user data access.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register(self, *, email: str, password: str) -> User:
        """
        Register a new user.

        Input:
        - `email`: unique user email.
        - `password`: plain password from request.

        Output:
        - Created `User` entity.

        Raises:
        - `ConflictError` if email is already registered.
        """

        existing = self.user_repository.get_by_email(email)
        if existing:
            raise ConflictError("An account with this email already exists.")

        password_hash = hash_password(password)
        return self.user_repository.create(email=email, password_hash=password_hash)

    def login(self, *, email: str, password: str) -> str:
        """
        Validate credentials and return an access token.

        Input:
        - `email`: user email.
        - `password`: plain password.

        Output:
        - JWT access token string.

        Raises:
        - `UnauthorizedError` if credentials are invalid.
        """

        user = self.user_repository.get_by_email(email)
        if not user:
            raise UnauthorizedError("Invalid email or password.")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password.")

        return create_access_token(subject=str(user.id))

