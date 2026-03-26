"""
API v1 router aggregator.

What this file does:
- Collects all v1 route modules (auth, expenses, categories, etc.) into one router.

Why it is needed:
- Keeps `main.py` small and focused.
- Makes it easy to add new modules without touching the app bootstrap code.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.expenses import router as expenses_router

router = APIRouter()

# Current modules
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(categories_router, prefix="/categories", tags=["categories"])
router.include_router(expenses_router, prefix="/expenses", tags=["expenses"])


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """
    Lightweight health check endpoint.

    Output:
    - Simple JSON response used by load balancers / uptime checks.
    """

    return {"status": "ok"}

