"""
SQLAlchemy declarative base.

What this file does:
- Exposes `Base` and imports all model modules once.

Why it is needed:
- Ensures `Base.metadata` contains every table definition.
- Keeps migration tooling and startup table creation reliable.
"""

from app.db.base_class import Base

# Import model modules so SQLAlchemy registers all tables on Base.metadata.
from app.models import category, expense, user  # noqa: E402,F401

