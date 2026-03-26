"""
Global exception handlers for FastAPI.

What this file does:
- Defines exception handlers that turn Python exceptions into consistent JSON responses.

Why it is needed:
- Keeps controllers clean (they can raise domain errors and let middleware handle them).
- Produces consistent error shapes for frontend/mobile clients.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.utils.errors import (
    AppError,
    ConflictError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)

logger = logging.getLogger(__name__)


def _error_payload(*, code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    """
    Standardize error responses.

    Output:
    - A JSON-serializable dict with a stable shape.
    """

    payload: dict[str, Any] = {"error": {"code": code, "message": message}}
    if details is not None:
        payload["error"]["details"] = details
    return payload


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    """
    Handle domain/service layer errors.

    Inputs:
    - `exc`: error raised in repositories/services

    Output:
    - JSONResponse with appropriate HTTP status + stable error payload
    """

    if isinstance(exc, NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=_error_payload(code="NOT_FOUND", message=exc.message),
        )
    if isinstance(exc, ConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=_error_payload(code="CONFLICT", message=exc.message),
        )
    if isinstance(exc, UnauthorizedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=_error_payload(code="UNAUTHORIZED", message=exc.message),
        )
    if isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_error_payload(code="VALIDATION_ERROR", message=exc.message),
        )

    # Default for unknown AppError subclasses
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=_error_payload(code="APP_ERROR", message=exc.message),
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected errors.

    Why log?
    - The client should get a generic message.
    - The server logs should contain full details for debugging.
    """

    logger.exception("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_payload(code="INTERNAL_SERVER_ERROR", message="Something went wrong."),
    )

