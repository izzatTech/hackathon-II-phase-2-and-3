"""
Authentication middleware for the Todo application.
Provides authentication and authorization checks for protected routes.
"""

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import uuid
from backend.src.utils.auth import verify_access_token


security = HTTPBearer()


async def get_current_user_id(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user ID from the authentication token.

    Args:
        request (Request): The incoming request
        credentials (HTTPAuthorizationCredentials): The authorization credentials from the request

    Returns:
        str: The user ID extracted from the token

    Raises:
        HTTPException: If the token is invalid or expired
    """
    token = credentials.credentials

    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


def require_authentication(request: Request, current_user_id: str = Depends(get_current_user_id)) -> str:
    """
    Middleware function to require authentication for protected routes.

    Args:
        request (Request): The incoming request
        current_user_id (str): The user ID from the authentication token

    Returns:
        str: The user ID for use in route handlers

    Raises:
        HTTPException: If the user is not authenticated
    """
    # This function can be used as a dependency in routes that require authentication
    # It simply returns the current user ID if the user is authenticated
    return current_user_id


def require_same_user_or_admin(target_user_id: str, current_user_id: str = Depends(require_authentication)) -> bool:
    """
    Middleware function to ensure that the current user is either the target user or an admin.

    Args:
        target_user_id (str): The ID of the user whose resources are being accessed
        current_user_id (str): The ID of the currently authenticated user

    Returns:
        bool: True if the current user has permission to access the target user's resources

    Raises:
        HTTPException: If the user doesn't have permission to access the resources
    """
    # Convert string UUIDs to UUID objects for comparison
    try:
        target_uuid = uuid.UUID(target_user_id)
        current_uuid = uuid.UUID(current_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Check if the current user is the same as the target user
    if current_uuid != target_uuid:
        # In a real application, you might also check if the current user is an admin
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this resource"
        )

    return True