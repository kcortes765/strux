"""
PAZ Application Bootstrap.

This module initializes and runs the FastAPI application.
"""

from typing import TYPE_CHECKING

from paz.core.constants import API_V1_PREFIX, APP_NAME, DESCRIPTION, VERSION
from paz.core.logging_config import get_logger, setup_logging


if TYPE_CHECKING:
    from fastapi import FastAPI


def create_app() -> "FastAPI":
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    # Setup logging
    setup_logging(level="INFO")
    logger = get_logger("app")

    logger.info(f"Initializing {APP_NAME} v{VERSION}")

    # Create FastAPI app
    app = FastAPI(
        title=APP_NAME,
        description=DESCRIPTION,
        version=VERSION,
        docs_url=f"{API_V1_PREFIX}/docs",
        redoc_url=f"{API_V1_PREFIX}/redoc",
        openapi_url=f"{API_V1_PREFIX}/openapi.json",
    )

    # Configure CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # Frontend dev server
            "http://localhost:5173",  # Vite dev server
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint for load balancers and monitoring."""
        return {
            "status": "healthy",
            "app": APP_NAME,
            "version": VERSION,
        }

    # Root endpoint
    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint with API information."""
        return {
            "app": APP_NAME,
            "version": VERSION,
            "description": DESCRIPTION,
            "docs": f"{API_V1_PREFIX}/docs",
        }

    logger.info(f"{APP_NAME} initialized successfully")

    return app


def run_app() -> int:
    """
    Run the PAZ application.

    Returns:
        Exit code (0 for success)
    """
    import uvicorn

    from paz.core.logging_config import get_logger

    logger = get_logger("main")
    logger.info(f"Starting {APP_NAME} server...")

    try:
        uvicorn.run(
            "paz.app:create_app",
            factory=True,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
        return 0
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Server error: {e}")
        return 1


# For uvicorn direct execution: uvicorn paz.app:app
app = create_app()
