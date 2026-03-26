"""
Error types used across the application.

What this file does:
- Defines application-specific exceptions (domain/service errors).

Why it is needed:
- Services should raise meaningful errors (not HTTP exceptions directly).
- Controllers translate these errors into HTTP responses (clean architecture).
"""


class AppError(Exception):
    """
    Base class for application errors.

 Inputs:
 - message: human-readable error message

 Output:
 - Exception instance that can be handled globally
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""


class ConflictError(AppError):
    """Raised when a request conflicts with current state (e.g., duplicate email)."""


class UnauthorizedError(AppError):
    """Raised when authentication/authorization fails."""


class ValidationError(AppError):
    """Raised when business rules validation fails."""

