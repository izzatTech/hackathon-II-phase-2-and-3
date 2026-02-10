"""
Task schemas for the Todo application.
Defines Pydantic models for Task API requests and responses.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid
from enum import Enum   # ✅ IMPORTANT


class TaskStatus(str, Enum):   # ✅ FIXED
    """Enum for task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):   # ✅ FIXED
    """Enum for task priority values."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskBase(BaseModel):
    """Base schema for Task with shared attributes."""
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task response with additional fields."""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {          # ✅ Pydantic v2
        "from_attributes": True
    }
