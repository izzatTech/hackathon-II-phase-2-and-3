"""
CORS middleware configuration for the Todo application.
Sets up Cross-Origin Resource Sharing policies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os


def setup_cors(app: FastAPI) -> None:
    """
    Setup CORS middleware for the application.

    Args:
        app (FastAPI): The FastAPI application instance
    """
    # Get allowed origins from environment variable or use default
    allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
    if allowed_origins_env:
        allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
    else:
        # Default allowed origins - in production, configure these properly
        allowed_origins = [
            "http://localhost:3000",  # Default Next.js dev server
            "http://localhost:8000",  # Default backend server
            "http://localhost:8080",  # Alternative dev server
            "https://localhost:3000",
            "https://localhost:8000",
            "https://localhost:8080",
        ]

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],  # In production, specify exact methods needed
        allow_headers=["*"],  # In production, specify exact headers needed
    )