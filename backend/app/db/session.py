"""
Database engine + session management.

What this file does:
- Creates the SQLAlchemy engine from `DATABASE_URL`.
- Provides `SessionLocal` (session factory) and a FastAPI dependency `get_db()`.

Why it is needed:
- Clean architecture wants repositories/services to receive a DB session via dependency injection.
- A single source of truth for DB configuration avoids subtle connection issues.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings


# `pool_pre_ping=True` helps recover from dropped MySQL connections.
engine = create_engine(settings.database_url, pool_pre_ping=True)

# `autocommit=False` and `autoflush=False` are common defaults for web apps.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session per request.

    How to use:
    - In controllers/routers: `db: Session = Depends(get_db)`

    Lifecycle:
    - Creates a session at the beginning of a request
    - Yields it to your code
    - Ensures it is closed even if an exception occurs
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

