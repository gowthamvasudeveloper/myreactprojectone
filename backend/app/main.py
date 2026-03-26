"""
FastAPI application entrypoint.

What this file does:
- Creates the FastAPI app instance
- Configures logging
- Registers API routers (versioned under /api/v1)
- Registers global exception handlers

Why it is needed:
- This is the single, predictable place your ASGI server (uvicorn) imports.
- Keeping bootstrap code here supports clean architecture: routes call controllers,
  controllers call services, services call repositories.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.logging import configure_logging
from app.core.settings import settings
from app.db.init_db import create_db_and_tables
from app.middleware.exception_handler import app_error_handler, unhandled_exception_handler
from app.utils.errors import AppError


def create_app() -> FastAPI:
    """
    App factory.

    Why a factory?
    - Makes testing easier (you can create an app with test settings).
    - Avoids side effects at import time (important for workers and tooling).
    """

    configure_logging()

    app = FastAPI(title=settings.app_name)

    # CORS middleware allows browser preflight (OPTIONS) + cross-origin requests.
    # Example: frontend on localhost:3000 calling backend on localhost:8000.
    cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Versioned API router
    app.include_router(v1_router, prefix=settings.api_v1_prefix)

    @app.on_event("startup")
    def on_startup() -> None:
        """
        Startup hook for local bootstrapping.

        Note:
        - For enterprise production systems, Alembic migrations are preferred.
        - For this stage, this ensures tables exist when the app starts.
        """

        create_db_and_tables()

    # Global exception handlers
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    return app


app = create_app()

