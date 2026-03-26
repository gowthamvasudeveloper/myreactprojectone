"""
Expense service (business logic layer).

What this file does:
- Implements expense business rules, ownership checks, filtering, and pagination behavior.

Why it is needed:
- Keeps controllers thin and centralizes domain rules in one place.
"""

from __future__ import annotations

from datetime import date

from app.models import Expense, User
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository
from app.utils.errors import NotFoundError, ValidationError


class ExpenseService:
    """
    Expense business logic.
    """

    def __init__(
        self,
        expense_repository: ExpenseRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self.expense_repository = expense_repository
        self.category_repository = category_repository

    def _validate_category_ownership(self, *, current_user: User, category_id: int | None) -> None:
        """
        Ensure category belongs to current user when provided.
        """

        if category_id is None:
            return

        category = self.category_repository.get_by_id(category_id)
        if not category or category.user_id != current_user.id:
            raise ValidationError("Invalid category for current user.")

    def create_expense(
        self,
        *,
        current_user: User,
        category_id: int | None,
        amount,
        expense_date: date,
        description: str | None,
    ) -> Expense:
        """
        Create a new expense owned by current user.
        """

        self._validate_category_ownership(current_user=current_user, category_id=category_id)
        return self.expense_repository.create(
            user_id=current_user.id,
            category_id=category_id,
            amount=amount,
            expense_date=expense_date,
            description=description,
        )

    def get_expense(self, *, current_user: User, expense_id: int) -> Expense:
        """
        Return one expense if it belongs to current user.
        """

        expense = self.expense_repository.get_by_id(expense_id)
        if not expense or expense.user_id != current_user.id:
            raise NotFoundError("Expense not found.")
        return expense

    def update_expense(
        self,
        *,
        current_user: User,
        expense_id: int,
        category_id: int | None,
        amount,
        expense_date: date,
        description: str | None,
    ) -> Expense:
        """
        Update an existing expense after ownership and validation checks.
        """

        expense = self.get_expense(current_user=current_user, expense_id=expense_id)
        self._validate_category_ownership(current_user=current_user, category_id=category_id)
        return self.expense_repository.update(
            expense,
            category_id=category_id,
            amount=amount,
            expense_date=expense_date,
            description=description,
        )

    def delete_expense(self, *, current_user: User, expense_id: int) -> None:
        """
        Delete an expense if it belongs to current user.
        """

        expense = self.get_expense(current_user=current_user, expense_id=expense_id)
        self.expense_repository.delete(expense)

    def list_expenses(
        self,
        *,
        current_user: User,
        date_from: date | None,
        date_to: date | None,
        category_id: int | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Expense], int]:
        """
        Return filtered + paginated expense list for current user.
        """

        if date_from and date_to and date_from > date_to:
            raise ValidationError("`date_from` cannot be greater than `date_to`.")

        if category_id is not None:
            self._validate_category_ownership(current_user=current_user, category_id=category_id)

        return self.expense_repository.list_filtered(
            user_id=current_user.id,
            date_from=date_from,
            date_to=date_to,
            category_id=category_id,
            page=page,
            page_size=page_size,
        )

