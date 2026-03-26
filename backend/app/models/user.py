"""
User ORM model (database table).

What this file does:
- Defines the `User` SQLAlchemy ORM model.

Why it is needed:
- Users own expenses and categories.
- Authentication is tied to a user identity (email + password hash).

Beginner-friendly note:
- Think of this class as "the database representation" of a user.
- We store `password_hash` (NOT the plain password).
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class User(Base):
    """
    Represents a user in the database.

    Inputs:
    - Instances are created by your service layer (e.g. during registration).

    Outputs:
    - Rows in the `users` table.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Email is used as the login identity.
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    # Store a bcrypt hash, never the plain password.
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

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
    categories: Mapped[List["Category"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    expenses: Mapped[List["Expense"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

