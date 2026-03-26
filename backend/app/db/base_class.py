"""
Pure SQLAlchemy declarative base class.

What this file does:
- Defines the `Base` class without importing any model modules.

Why it is needed:
- Prevents circular imports between models and metadata bootstrap files.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Shared base class for all ORM models.
    """

    pass

