"""
Task model for the Todo application.
Defines the Task entity with all required fields and relationships.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
from enum import Enum


class TaskStatus(Enum):
    """Enum for task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(Enum):
    """Enum for task priority values."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


if TYPE_CHECKING:
    from backend.src.models.user import User


class TaskBase(SQLModel):
    """Base class for Task model with shared attributes."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """Task model with database table configuration."""
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    # Relationship to User
    user: "User" = Relationship(back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status.value}')>"

    @classmethod
    def from_orm(cls, obj):
        """Convert ORM object to Pydantic model."""
        return cls(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            status=obj.status,
            priority=obj.priority,
            user_id=obj.user_id,
            due_date=obj.due_date,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )