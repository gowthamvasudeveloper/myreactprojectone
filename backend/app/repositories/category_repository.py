"""
Category repository (database access layer).

What this file does:
- Encapsulates all category-related SQLAlchemy queries.

Why it is needed:
- Keeps SQL/ORM query logic out of services/controllers.
- Improves maintainability and testability.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category


class CategoryRepository:
    """
    Repository for category data access.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_user(self, user_id: int) -> list[Category]:
        """
        Return all categories owned by a user.
        """

        stmt = select(Category).where(Category.user_id == user_id).order_by(Category.name.asc())
        return list(self.db.execute(stmt).scalars().all())

    def get_by_id(self, category_id: int) -> Category | None:
        """
        Return category by primary key.
        """

        stmt = select(Category).where(Category.id == category_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_user_and_name(self, *, user_id: int, name: str) -> Category | None:
        """
        Return one category by (user_id, name) if it exists.
        """

        stmt = select(Category).where(Category.user_id == user_id, Category.name == name)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, *, user_id: int, name: str) -> Category:
        """
        Insert a new category and return persisted entity.
        """

        category = Category(user_id=user_id, name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category, *, name: str) -> Category:
        """
        Update an existing category name.
        """

        category.name = name
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        """
        Delete a category entity.
        """

        self.db.delete(category)
        self.db.commit()

