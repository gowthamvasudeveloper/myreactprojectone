"""
Category ORM model (database table).

What this file does:
- Defines the `Category` SQLAlchemy ORM model.

Why it is needed:
- Expenses are easier to analyze/report when grouped into categories.
- Categories are user-scoped (each user maintains their own set).
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Category(Base):
    """
    Represents an expense category owned by a specific user.

    Business rule:
    - A user cannot have two categories with the same name.
      (enforced by a unique constraint on (user_id, name)).
    """

    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_categories_user_id_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

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
    user: Mapped["User"] = relationship(back_populates="categories")
    expenses: Mapped[List["Expense"]] = relationship(back_populates="category")

