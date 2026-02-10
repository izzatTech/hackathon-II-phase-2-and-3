"""
Authentication service for the Todo application.
Handles user registration, login, logout, and session management.
"""

from datetime import timedelta
from typing import Optional
from sqlmodel import Session
from backend.src.models.user import User
from backend.src.repositories.user_repository import UserRepository
from backend.src.utils.auth import verify_password, get_password_hash, create_access_token
from backend.src.services.session_service import SessionService
import uuid


class AuthService:
    """Service class for handling authentication operations."""

    def __init__(self, session: Session, user_repo: UserRepository, session_service: SessionService):
        """
        Initialize the AuthService.

        Args:
            session (Session): Database session
            user_repo (UserRepository): User repository
            session_service (SessionService): Session service
        """
        self.session = session
        self.user_repo = user_repo
        self.session_service = session_service

    def register_user(self, email: str, username: str, password: str) -> Optional[User]:
        """
        Register a new user.

        Args:
            email (str): User's email address
            username (str): User's chosen username
            password (str): User's password

        Returns:
            Optional[User]: The created user if successful, None otherwise
        """
        # Check if user with this email already exists
        existing_user = self.user_repo.get_user_by_email(email)
        if existing_user:
            return None  # User with this email already exists

        # Check if user with this username already exists
        existing_user = self.user_repo.get_user_by_username(username)
        if existing_user:
            return None  # User with this username already exists

        # Hash the password
        hashed_password = get_password_hash(password)

        # Create user data
        user_data = {
            'email': email,
            'username': username,
            'hashed_password': hashed_password
        }

        # Create the user in the database
        new_user = self.user_repo.create_user(user_data)

        return new_user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            email (str): User's email address
            password (str): User's password

        Returns:
            Optional[User]: The authenticated user if successful, None otherwise
        """
        # Retrieve the user from the database
        user = self.user_repo.get_user_by_email(email)

        # If user exists and password is correct, return the user
        if user and verify_password(password, user.hashed_password):
            return user

        # Authentication failed
        return None

    def login_user(self, email: str, password: str) -> Optional[dict]:
        """
        Login a user and return an access token.

        Args:
            email (str): User's email address
            password (str): User's password

        Returns:
            Optional[dict]: Dictionary containing access token if successful, None otherwise
        """
        user = self.authenticate_user(email, password)

        if not user:
            return None

        # Create an access token for the user
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        # Create session in database (optional depending on requirements)
        # This would involve creating a session record with the session_service

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "username": user.username
        }

    def logout_user(self, user_id: str) -> bool:
        """
        Logout a user (invalidate their session).

        Args:
            user_id (str): The ID of the user to logout

        Returns:
            bool: True if logout was successful, False otherwise
        """
        # In a real implementation, this might involve invalidating the session in the database
        # For JWT-based auth, we typically rely on token expiration, but we could maintain
        # a blacklist of invalidated tokens

        # Return True to indicate success
        return True

    def refresh_access_token(self, user_id: str) -> Optional[str]:
        """
        Refresh an access token for a user.

        Args:
            user_id (str): The ID of the user to refresh token for

        Returns:
            Optional[str]: New access token if successful, None otherwise
        """
        # Validate that the user exists
        user = self.user_repo.get_user_by_id(uuid.UUID(user_id))

        if not user:
            return None

        # Create a new access token
        access_token_expires = timedelta(minutes=30)
        new_access_token = create_access_token(
            data={"sub": user_id}, expires_delta=access_token_expires
        )

        return new_access_token