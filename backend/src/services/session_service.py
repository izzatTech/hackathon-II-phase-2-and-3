"""
Session service for the Todo application.
Manages user sessions and authentication state.
"""

from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session
from backend.src.models.session import SessionModel
from backend.src.utils.auth import create_access_token
import uuid
import secrets


class SessionService:
    """Service class for handling session operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the SessionService.

        Args:
            db_session (Session): Database session
        """
        self.db_session = db_session

    def create_session(self, user_id: uuid.UUID, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Optional[SessionModel]:
        """
        Create a new user session.

        Args:
            user_id (uuid.UUID): The ID of the user for whom to create a session
            ip_address (Optional[str]): The IP address of the client
            user_agent (Optional[str]): The user agent string of the client

        Returns:
            Optional[SessionModel]: The created session if successful, None otherwise
        """
        # Generate a random session token
        session_token = secrets.token_urlsafe(32)

        # Set session expiry (e.g., 30 days from creation)
        expires_at = datetime.utcnow() + timedelta(days=30)

        # Create session data
        session_data = {
            "user_id": user_id,
            "token": session_token,
            "expires_at": expires_at,
            "ip_address": ip_address,
            "user_agent": user_agent
        }

        # Create session model
        session = SessionModel(**session_data)

        # Save to database
        self.db_session.add(session)
        self.db_session.commit()
        self.db_session.refresh(session)

        return session

    def get_session_by_token(self, token: str) -> Optional[SessionModel]:
        """
        Get a session by its token.

        Args:
            token (str): The session token

        Returns:
            Optional[SessionModel]: The session if found and valid, None otherwise
        """
        # Query for the session with the given token
        from sqlmodel import select
        statement = select(SessionModel).where(
            SessionModel.token == token,
            SessionModel.expires_at > datetime.utcnow()  # Ensure session hasn't expired
        )

        session = self.db_session.exec(statement).first()
        return session

    def get_session_by_user_id(self, user_id: uuid.UUID) -> Optional[SessionModel]:
        """
        Get a session by user ID.

        Args:
            user_id (uuid.UUID): The user ID

        Returns:
            Optional[SessionModel]: The session if found and valid, None otherwise
        """
        from sqlmodel import select
        statement = select(SessionModel).where(
            SessionModel.user_id == user_id,
            SessionModel.expires_at > datetime.utcnow()  # Ensure session hasn't expired
        )

        session = self.db_session.exec(statement).first()
        return session

    def invalidate_session(self, token: str) -> bool:
        """
        Invalidate a session by removing it from the database.

        Args:
            token (str): The session token to invalidate

        Returns:
            bool: True if the session was successfully invalidated, False otherwise
        """
        session = self.get_session_by_token(token)

        if session:
            self.db_session.delete(session)
            self.db_session.commit()
            return True

        return False

    def invalidate_all_sessions_for_user(self, user_id: uuid.UUID) -> bool:
        """
        Invalidate all sessions for a given user.

        Args:
            user_id (uuid.UUID): The ID of the user whose sessions to invalidate

        Returns:
            bool: True if sessions were successfully invalidated, False otherwise
        """
        from sqlmodel import select
        statement = select(SessionModel).where(
            SessionModel.user_id == user_id
        )

        sessions = self.db_session.exec(statement).all()

        for session in sessions:
            self.db_session.delete(session)

        self.db_session.commit()
        return len(sessions) > 0

    def refresh_session(self, token: str) -> Optional[SessionModel]:
        """
        Refresh a session by extending its expiry time.

        Args:
            token (str): The session token to refresh

        Returns:
            Optional[SessionModel]: The refreshed session if successful, None otherwise
        """
        session = self.get_session_by_token(token)

        if session:
            # Extend the session expiry time
            session.expires_at = datetime.utcnow() + timedelta(days=30)

            # Update the session in the database
            self.db_session.add(session)
            self.db_session.commit()
            self.db_session.refresh(session)

            return session

        return None