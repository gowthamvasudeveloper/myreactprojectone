"""
Expense repository (database access layer).

What this file does:
- Encapsulates all expense-related SQLAlchemy queries.
- Supports filtered/paginated listing.

Why it is needed:
- Keeps data access concerns out of service/controller layers.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Expense


class ExpenseRepository:
    """
    Repository for expense data operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, expense_id: int) -> Expense | None:
        """
        Return one expense by primary key.
        """

        stmt = select(Expense).where(Expense.id == expense_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(
        self,
        *,
        user_id: int,
        category_id: int | None,
        amount,
        expense_date: date,
        description: str | None,
    ) -> Expense:
        """
        Insert a new expense and return persisted entity.
        """

        expense = Expense(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            expense_date=expense_date,
            description=description,
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def update(
        self,
        expense: Expense,
        *,
        category_id: int | None,
        amount,
        expense_date: date,
        description: str | None,
    ) -> Expense:
        """
        Update an expense row and return refreshed entity.
        """

        expense.category_id = category_id
        expense.amount = amount
        expense.expense_date = expense_date
        expense.description = description
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete(self, expense: Expense) -> None:
        """
        Delete an expense row.
        """

        self.db.delete(expense)
        self.db.commit()

    def list_filtered(
        self,
        *,
        user_id: int,
        date_from: date | None,
        date_to: date | None,
        category_id: int | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Expense], int]:
        """
        Return paginated expenses + total count for filters.
        """

        filters = [Expense.user_id == user_id]
        if date_from is not None:
            filters.append(Expense.expense_date >= date_from)
        if date_to is not None:
            filters.append(Expense.expense_date <= date_to)
        if category_id is not None:
            filters.append(Expense.category_id == category_id)

        count_stmt = select(func.count()).select_from(Expense).where(*filters)
        total = int(self.db.execute(count_stmt).scalar_one())

        stmt = (
            select(Expense)
            .where(*filters)
            .order_by(Expense.expense_date.desc(), Expense.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        expenses = list(self.db.execute(stmt).scalars().all())
        return expenses, total

