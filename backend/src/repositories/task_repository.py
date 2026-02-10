"""
Task repository for the Todo application.
Handles all database operations for Task entities.
"""

from typing import List, Optional
from sqlmodel import Session, select
from backend.src.models.task import Task
from backend.src.schemas.task import TaskCreate, TaskUpdate
from backend.src.models.user import User
import uuid


class TaskRepository:
    """Repository class for handling Task database operations."""

    def __init__(self, session: Session):
        """
        Initialize the TaskRepository.

        Args:
            session (Session): Database session
        """
        self.session = session

    def create_task(self, task_data: TaskCreate, user_id: uuid.UUID) -> Task:
        """
        Create a new task.

        Args:
            task_data (TaskCreate): Task creation data
            user_id (uuid.UUID): ID of the user creating the task

        Returns:
            Task: The created task
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            user_id=user_id,
            due_date=task_data.due_date
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_task_by_id(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """
        Get a task by its ID for a specific user.

        Args:
            task_id (uuid.UUID): ID of the task
            user_id (uuid.UUID): ID of the user

        Returns:
            Optional[Task]: The task if found and belongs to the user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return self.session.exec(statement).first()

    def get_tasks_by_user(
        self,
        user_id: uuid.UUID,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Task]:
        """
        Get tasks for a specific user with optional filtering.

        Args:
            user_id (uuid.UUID): ID of the user
            status (Optional[str]): Filter by status
            priority (Optional[str]): Filter by priority
            limit (int): Number of tasks to return
            offset (int): Offset for pagination

        Returns:
            List[Task]: List of tasks matching the criteria
        """
        statement = select(Task).where(Task.user_id == user_id)

        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)

        statement = statement.offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def update_task(self, task_id: uuid.UUID, user_id: uuid.UUID, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update a task.

        Args:
            task_id (uuid.UUID): ID of the task to update
            user_id (uuid.UUID): ID of the user (for authorization)
            task_data (TaskUpdate): Task update data

        Returns:
            Optional[Task]: The updated task if found and authorized, None otherwise
        """
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        # Update only provided fields
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        # Update the timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """
        Delete a task.

        Args:
            task_id (uuid.UUID): ID of the task to delete
            user_id (uuid.UUID): ID of the user (for authorization)

        Returns:
            bool: True if task was deleted, False otherwise
        """
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def complete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """
        Mark a task as completed.

        Args:
            task_id (uuid.UUID): ID of the task to complete
            user_id (uuid.UUID): ID of the user (for authorization)

        Returns:
            Optional[Task]: The updated task if found and authorized, None otherwise
        """
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        task.status = "completed"
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task