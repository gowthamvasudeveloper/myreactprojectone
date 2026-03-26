"""
Category endpoints (controller layer).

What this file does:
- Exposes CRUD endpoints for user categories.

Why it is needed:
- Categories are required for organizing and filtering expenses.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("", response_model=list[CategoryRead], status_code=status.HTTP_200_OK)
def list_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CategoryRead]:
    """
    Return current user's categories.
    """

    service = CategoryService(CategoryRepository(db))
    categories = service.list_categories(current_user=current_user)
    return [CategoryRead.model_validate(item) for item in categories]


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CategoryRead:
    """
    Create a category for current user.
    """

    service = CategoryService(CategoryRepository(db))
    category = service.create_category(current_user=current_user, name=payload.name)
    return CategoryRead.model_validate(category)


@router.patch("/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CategoryRead:
    """
    Update category name.
    """

    if payload.name is None:
        # Keep 422 style for invalid payload semantics
        from app.utils.errors import ValidationError

        raise ValidationError("At least one field must be provided for update.")

    service = CategoryService(CategoryRepository(db))
    category = service.update_category(
        current_user=current_user,
        category_id=category_id,
        name=payload.name,
    )
    return CategoryRead.model_validate(category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    """
    Delete a category owned by current user.
    """

    service = CategoryService(CategoryRepository(db))
    service.delete_category(current_user=current_user, category_id=category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

