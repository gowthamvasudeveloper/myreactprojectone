"""
Application logging configuration.

What this file does:
- Configures Python's standard logging module in a consistent way.

Why it is needed:
- In production, logs are your primary debugging/observability tool.
- Centralized configuration keeps log format and verbosity consistent.
"""

from __future__ import annotations

import logging
import sys

from app.core.settings import settings


def configure_logging() -> None:
    """
    Configure global logging settings for the application.

    Inputs:
    - `settings.log_level` (string like "INFO" or "DEBUG")

    Output:
    - No return value; sets up global logging handlers/format.
    """

    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # A simple, production-friendly format. In real production you might output JSON.
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    root = logging.getLogger()
    root.setLevel(level)

    # Avoid duplicate handlers in reload/dev environments.
    root.handlers = []
    root.addHandler(handler)

