"""
Schemas package.

What this file does:
- Re-exports Pydantic schemas for convenient imports.

Why it is needed:
- Keeps imports consistent across controllers/services.
"""

from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.schemas.expense import ExpenseCreate, ExpenseListResponse, ExpenseRead, ExpenseUpdate
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserCreate, UserRead

__all__ = [
    "UserCreate",
    "UserRead",
    "RegisterRequest",
    "LoginRequest",
    "TokenResponse",
    "CategoryCreate",
    "CategoryRead",
    "CategoryUpdate",
    "ExpenseCreate",
    "ExpenseRead",
    "ExpenseListResponse",
    "ExpenseUpdate",
]

