"""
Expense endpoints (controller layer).

What this file does:
- Exposes CRUD and filtered/paginated listing endpoints for expenses.

Why it is needed:
- Expenses are the main business resource in this application.
"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate, ExpenseListResponse, ExpenseRead, ExpenseUpdate
from app.services.expense_service import ExpenseService
from app.utils.errors import ValidationError

router = APIRouter()


def _build_expense_service(db: Session) -> ExpenseService:
    """
    Create service with required repositories.
    """

    return ExpenseService(
        expense_repository=ExpenseRepository(db),
        category_repository=CategoryRepository(db),
    )


@router.get("", response_model=ExpenseListResponse, status_code=status.HTTP_200_OK)
def list_expenses(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    category_id: int | None = Query(default=None, ge=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExpenseListResponse:
    """
    Return filtered, paginated expense list for current user.
    """

    service = _build_expense_service(db)
    items, total = service.list_expenses(
        current_user=current_user,
        date_from=date_from,
        date_to=date_to,
        category_id=category_id,
        page=page,
        page_size=page_size,
    )
    return ExpenseListResponse(
        items=[ExpenseRead.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{expense_id}", response_model=ExpenseRead, status_code=status.HTTP_200_OK)
def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExpenseRead:
    """
    Return a single expense by id (must belong to current user).
    """

    service = _build_expense_service(db)
    expense = service.get_expense(current_user=current_user, expense_id=expense_id)
    return ExpenseRead.model_validate(expense)


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExpenseRead:
    """
    Create a new expense for current user.
    """

    service = _build_expense_service(db)
    expense = service.create_expense(
        current_user=current_user,
        category_id=payload.category_id,
        amount=payload.amount,
        expense_date=payload.expense_date,
        description=payload.description,
    )
    return ExpenseRead.model_validate(expense)


@router.patch("/{expense_id}", response_model=ExpenseRead, status_code=status.HTTP_200_OK)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExpenseRead:
    """
    Update expense fields. Missing fields keep existing values.
    """

    service = _build_expense_service(db)
    current = service.get_expense(current_user=current_user, expense_id=expense_id)

    if not payload.model_fields_set:
        raise ValidationError("At least one field must be provided for update.")

    expense = service.update_expense(
        current_user=current_user,
        expense_id=expense_id,
        category_id=payload.category_id if "category_id" in payload.model_fields_set else current.category_id,
        amount=payload.amount if payload.amount is not None else current.amount,
        expense_date=payload.expense_date if payload.expense_date is not None else current.expense_date,
        description=payload.description if "description" in payload.model_fields_set else current.description,
    )
    return ExpenseRead.model_validate(expense)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    """
    Delete an expense owned by current user.
    """

    service = _build_expense_service(db)
    service.delete_expense(current_user=current_user, expense_id=expense_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

