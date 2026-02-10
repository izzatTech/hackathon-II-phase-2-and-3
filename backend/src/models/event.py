"""
Event model for the Todo application.
Defines the Event entity for event-driven architecture.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid

if TYPE_CHECKING:
    from backend.src.models.user import User
    from backend.src.models.task import Task


class EventType(str):
    """Enum for event types."""
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_COMPLETED = "task_completed"
    USER_SIGNED_UP = "user_signed_up"


class Event(SQLModel, table=True):
    """Event model for system events."""
    __tablename__ = "events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_type: str = Field(max_length=50, nullable=False)  # Using str instead of enum for flexibility
    entity_id: str = Field(max_length=100, nullable=False)
    entity_type: str = Field(max_length=50, nullable=False)  # 'task', 'user', etc.
    payload_json: str = Field(sa_column_kwargs={"nullable": False})  # Store event data as JSON string
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    processed: bool = Field(default=False)  # Flag to track if event has been processed

    def __repr__(self):
        return f"<Event(id={self.id}, type='{self.event_type}', entity_id='{self.entity_id}')>"

    @classmethod
    def from_orm(cls, obj):
        """Convert ORM object to Pydantic model."""
        return cls(
            id=obj.id,
            event_type=obj.event_type,
            entity_id=obj.entity_id,
            entity_type=obj.entity_type,
            payload_json=obj.payload_json,
            created_at=obj.created_at,
            processed=obj.processed
        )