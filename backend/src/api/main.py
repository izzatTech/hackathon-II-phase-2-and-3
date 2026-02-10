"""
Main API router for the Todo application.
Aggregates all API routes and sets up the main application.
"""

from fastapi import FastAPI
from backend.src.api.auth import router as auth_router
from backend.src.api.tasks import router as tasks_router
from backend.src.api.chat import router as chat_router
from backend.src.middleware.cors import setup_cors
from backend.src.middleware.security import setup_security_headers
import os


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance
    """
    # Get the app title from environment variable or use default
    app_title = os.getenv("APP_TITLE", "Todo Application API")

    # Create the FastAPI application
    app = FastAPI(
        title=app_title,
        description="API for the Todo application with task management, authentication, and AI integration",
        version="1.0.0"
    )

    # Include API routers
    app.include_router(auth_router)
    app.include_router(tasks_router)
    app.include_router(chat_router)

    # Setup CORS middleware
    setup_cors(app)

    # Setup security headers
    setup_security_headers(app)

    return app


def setup_routes(app: FastAPI) -> None:
    """
    Setup all application routes.

    Args:
        app (FastAPI): The FastAPI application instance
    """
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """
        Health check endpoint to verify the API is running.

        Returns:
            dict: Health status information
        """
        return {"status": "healthy", "service": "Todo API"}

    # Root endpoint
    @app.get("/")
    async def root():
        """
        Root endpoint for the API.

        Returns:
            dict: Welcome message and API information
        """
        return {
            "message": "Welcome to the Todo Application API",
            "version": "1.0.0",
            "documentation": "/docs",
            "redoc": "/redoc"
        }


# Create the main application instance
app = create_app()
setup_routes(app)