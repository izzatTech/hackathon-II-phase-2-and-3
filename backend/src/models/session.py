"""
Session model for the Todo application.
Defines the Session entity with all required fields and relationships.
"""
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from backend.src.models.user import User


class SessionModel(SQLModel, table=True):
    """Session model for managing user sessions."""
    __tablename__ = "sessions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    token: str = Field(unique=True, nullable=False, max_length=500)
    expires_at: datetime = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=500)

    # Relationship to User
    user: "User" = Relationship(back_populates="sessions")

    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id})>"