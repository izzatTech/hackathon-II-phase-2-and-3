"""
User model for the Todo application.
Defines the User entity with all required fields and relationships.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid

if TYPE_CHECKING:
    from backend.src.models.task import Task
    from backend.src.models.session import SessionModel
    from backend.src.models.conversation import Conversation


class UserBase(SQLModel):
    """Base class for User model with shared attributes."""
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """User model with database table configuration."""
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    sessions: list["SessionModel"] = Relationship(back_populates="user")
    conversations: list["Conversation"] = Relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"

    @classmethod
    def from_orm(cls, obj):
        """Convert ORM object to Pydantic model."""
        return cls(
            id=obj.id,
            email=obj.email,
            username=obj.username,
            is_active=obj.is_active,
            hashed_password=obj.hashed_password,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )