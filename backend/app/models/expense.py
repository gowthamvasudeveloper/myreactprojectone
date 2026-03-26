"""
Expense ORM model (database table).

What this file does:
- Defines the `Expense` SQLAlchemy ORM model.

Why it is needed:
- Expenses are the primary business entity in this application.
- Expenses belong to a user and may be linked to a category.

Beginner-friendly note:
- `amount` uses a fixed-point numeric type to avoid floating point rounding errors.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Expense(Base):
    """
    Represents a single expense record.

    Typical use:
    - Created by a service method when a user submits an expense form.
    """

    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    # Category is optional: you may want to allow "uncategorized" expenses.
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), index=True, nullable=True
    )

    # Money should be stored as fixed precision (no floats).
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # A "business date" of the expense.
    expense_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)

    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="expenses")
    # Note:
    # - SQLAlchemy can struggle to interpret complex forward-reference annotations.
    # - Using Optional["Category"] keeps typing correct and is ORM-friendly.
    category: Mapped[Optional["Category"]] = relationship(back_populates="expenses")

