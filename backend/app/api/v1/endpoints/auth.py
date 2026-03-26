"""
Auth endpoints (controller layer).

What this file does:
- Exposes register/login/current-user endpoints under `/api/v1/auth`.

Why it is needed:
- Controllers map HTTP requests to service calls and shape API responses.
- They should stay thin and delegate business logic to services.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserRead:
    """
    Register endpoint.

    Input:
    - JSON payload with email/password.

    Output:
    - Public user object (without password hash).
    """

    service = AuthService(UserRepository(db))
    user = service.register(email=payload.email, password=payload.password)
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and return JWT token",
)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Login endpoint.

    Input:
    - JSON payload with email/password.

    Output:
    - JWT access token for Authorization header usage.
    """

    service = AuthService(UserRepository(db))
    access_token = service.login(email=payload.email, password=payload.password)
    return TokenResponse(access_token=access_token)


@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get currently authenticated user",
)
def read_current_user(current_user: User = Depends(get_current_user)) -> UserRead:
    """
    Return current authenticated user's profile.

    Input:
    - Bearer token in Authorization header.

    Output:
    - Public user profile.
    """

    return UserRead.model_validate(current_user)

