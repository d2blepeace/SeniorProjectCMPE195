"""
FastAPI application factory
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.config.settings import settings
from backend.src.utils.logger import logger


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application

    Returns:
        Configured FastAPI app instance
    """
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        debug=settings.debug,
        description="Smart Hydroponic Garden System API",
    )

    # CORS middleware - allows frontend to call API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info(f"FastAPI app created: {settings.app_name}")

    return app


# Create app instance
app = create_app()
