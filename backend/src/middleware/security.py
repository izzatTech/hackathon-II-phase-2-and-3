"""
Security headers middleware for the Todo application.
Adds security-related HTTP headers to responses.
"""

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security-related HTTP headers to responses.
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Set security headers
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        return response


def setup_security_headers(app: FastAPI) -> None:
    """
    Setup security headers middleware for the application.

    Args:
        app (FastAPI): The FastAPI application instance
    """
    app.add_middleware(SecurityHeadersMiddleware)