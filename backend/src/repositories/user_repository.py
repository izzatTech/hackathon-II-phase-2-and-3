"""
User repository for the Todo application.
Handles all database operations for User entities.
"""

from typing import Optional
from sqlmodel import Session, select
from backend.src.models.user import User
import uuid


class UserRepository:
    """Repository class for handling User database operations."""

    def __init__(self, session: Session):
        """
        Initialize the UserRepository.

        Args:
            session (Session): Database session
        """
        self.session = session

    def create_user(self, user_data: dict) -> User:
        """
        Create a new user.

        Args:
            user_data (dict): User creation data including hashed password

        Returns:
            User: The created user
        """
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            hashed_password=user_data['hashed_password']
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Get a user by their ID.

        Args:
            user_id (uuid.UUID): ID of the user

        Returns:
            Optional[User]: The user if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by their email.

        Args:
            email (str): Email of the user

        Returns:
            Optional[User]: The user if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by their username.

        Args:
            username (str): Username of the user

        Returns:
            Optional[User]: The user if found, None otherwise
        """
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    def update_user(self, user_id: uuid.UUID, user_data: dict) -> Optional[User]:
        """
        Update a user.

        Args:
            user_id (uuid.UUID): ID of the user to update
            user_data (dict): User update data

        Returns:
            Optional[User]: The updated user if found, None otherwise
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        # Update only provided fields
        for field, value in user_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        from datetime import datetime
        user.updated_at = datetime.utcnow()

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user(self, user_id: uuid.UUID) -> bool:
        """
        Delete a user.

        Args:
            user_id (uuid.UUID): ID of the user to delete

        Returns:
            bool: True if user was deleted, False otherwise
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        self.session.delete(user)
        self.session.commit()
        return True