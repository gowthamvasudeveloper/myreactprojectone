"""
Category service (business logic layer).

What this file does:
- Implements category business rules and ownership checks.

Why it is needed:
- Keeps controllers simple and enforces domain rules in one place.
"""

from __future__ import annotations

from app.models import Category, User
from app.repositories.category_repository import CategoryRepository
from app.utils.errors import ConflictError, NotFoundError, ValidationError


class CategoryService:
    """
    Category business logic.
    """

    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repository = category_repository

    def list_categories(self, *, current_user: User) -> list[Category]:
        """
        Return all categories for the current user.
        """

        return self.category_repository.list_by_user(current_user.id)

    def create_category(self, *, current_user: User, name: str) -> Category:
        """
        Create a category for current user after duplicate checks.
        """

        normalized_name = name.strip()
        if not normalized_name:
            raise ValidationError("Category name cannot be blank.")

        existing = self.category_repository.get_by_user_and_name(
            user_id=current_user.id, name=normalized_name
        )
        if existing:
            raise ConflictError("Category with this name already exists.")

        return self.category_repository.create(user_id=current_user.id, name=normalized_name)

    def update_category(self, *, current_user: User, category_id: int, name: str) -> Category:
        """
        Update a category if it belongs to current user.
        """

        category = self.category_repository.get_by_id(category_id)
        if not category or category.user_id != current_user.id:
            raise NotFoundError("Category not found.")

        normalized_name = name.strip()
        if not normalized_name:
            raise ValidationError("Category name cannot be blank.")

        existing = self.category_repository.get_by_user_and_name(
            user_id=current_user.id, name=normalized_name
        )
        if existing and existing.id != category.id:
            raise ConflictError("Category with this name already exists.")

        return self.category_repository.update(category, name=normalized_name)

    def delete_category(self, *, current_user: User, category_id: int) -> None:
        """
        Delete a category if it belongs to current user.
        """

        category = self.category_repository.get_by_id(category_id)
        if not category or category.user_id != current_user.id:
            raise NotFoundError("Category not found.")

        self.category_repository.delete(category)

