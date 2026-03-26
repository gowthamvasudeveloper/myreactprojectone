"""
Expense Pydantic schemas.

What this file does:
- Defines request/response models for expenses.

Why it is needed:
- Validates data types (amount/date/category) at the API boundary.
- Keeps a stable contract for future clients (web + mobile).
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    """
    Shared fields for expense schemas.
    """

    amount: Decimal = Field(gt=0)
    expense_date: date
    category_id: int | None = None
    description: str | None = Field(default=None, max_length=500)


class ExpenseCreate(ExpenseBase):
    """
    Payload for creating an expense.
    """

    pass


class ExpenseUpdate(BaseModel):
    """
    Payload for updating an expense (PATCH-like behavior).

    Input:
    - All fields optional so clients can update one field at a time.
    """

    amount: Decimal | None = Field(default=None, gt=0)
    expense_date: date | None = None
    category_id: int | None = None
    description: str | None = Field(default=None, max_length=500)


class ExpenseRead(ExpenseBase):
    """
    Public representation of an expense.
    """

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExpenseListResponse(BaseModel):
    """
    Paginated expense list response contract.

    Why this response shape:
    - Clients can render list data and page controls without extra endpoints.
    """

    items: list[ExpenseRead]
    total: int
    page: int
    page_size: int

