"""
Conversation and Message models for the Todo application.
Defines entities for AI-powered chat functionality.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
import uuid

if TYPE_CHECKING:
    from backend.src.models.user import User


class Conversation(SQLModel, table=True):
    """Conversation model for storing chat conversations."""
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    is_active: bool = Field(default=True)

    # Relationship to User
    user: "User" = Relationship(back_populates="conversations")

    # Relationship to Messages
    messages: List["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, title='{self.title}')>"


class Message(SQLModel, table=True):
    """Message model for storing individual messages in conversations."""
    __tablename__ = "messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    sender_type: str = Field(max_length=20)  # 'user', 'ai_assistant', or 'system'
    content: str = Field(max_length=5000)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    metadata_json: Optional[str] = Field(default=None)  # Store additional data as JSON string

    # Relationship to Conversation
    conversation: "Conversation" = Relationship(back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, sender_type='{self.sender_type}')>"

    @classmethod
    def from_orm(cls, obj):
        """Convert ORM object to Pydantic model."""
        return cls(
            id=obj.id,
            conversation_id=obj.conversation_id,
            sender_type=obj.sender_type,
            content=obj.content,
            created_at=obj.created_at,
            metadata_json=obj.metadata_json
        )