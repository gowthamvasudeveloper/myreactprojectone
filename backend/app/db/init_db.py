"""
Database bootstrap helpers.

What this file does:
- Provides a simple function to create tables from ORM metadata.

Why it is needed:
- Useful for local development/bootstrap before migrations are introduced.
"""

from __future__ import annotations

import logging
import time

from sqlalchemy.exc import OperationalError

from app.db.base import Base
from app.db.session import engine

logger = logging.getLogger(__name__)


def create_db_and_tables() -> None:
    """
    Create all tables defined by SQLAlchemy models.

    Output:
    - No return value; issues CREATE TABLE statements when tables do not exist.
    """

    # In container environments, DB may not be ready immediately.
    # We retry a few times to improve startup reliability.
    attempts = 10
    delay_seconds = 2

    for attempt in range(1, attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database schema initialization completed.")
            return
        except OperationalError:
            if attempt == attempts:
                logger.exception("Database not reachable after retries.")
                raise
            logger.warning(
                "Database not ready yet (attempt %s/%s). Retrying in %s seconds.",
                attempt,
                attempts,
                delay_seconds,
            )
            time.sleep(delay_seconds)

