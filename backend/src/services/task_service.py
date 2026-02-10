"""
Task service for the Todo application.
Handles business logic for task operations.
"""

from typing import List, Optional
from sqlmodel import Session
from backend.src.models.task import Task
from backend.src.schemas.task import TaskCreate, TaskUpdate
from backend.src.repositories.task_repository import TaskRepository
import uuid


class TaskService:
    """Service class for handling task business logic."""

    def __init__(self, session: Session):
        """
        Initialize the TaskService.

        Args:
            session (Session): Database session
        """
        self.session = session
        self.task_repo = TaskRepository(session)

    def create_task(self, task_data: TaskCreate, user_id: uuid.UUID) -> Task:
        """
        Create a new task with business logic validation.

        Args:
            task_data (TaskCreate): Task creation data
            user_id (uuid.UUID): ID of the user creating the task

        Returns:
            Task: The created task
        """
        # Add any business logic validation here before creating the task
        # For example, checking if the user can create more tasks, etc.

        return self.task_repo.create_task(task_data, user_id)

    def get_task_by_id(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """
        Get a task by its ID with authorization check.

        Args:
            task_id (uuid.UUID): ID of the task
            user_id (uuid.UUID): ID of the user requesting the task

        Returns:
            Optional[Task]: The task if found and authorized, None otherwise
        """
        return self.task_repo.get_task_by_id(task_id, user_id)

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
        return self.task_repo.get_tasks_by_user(user_id, status, priority, limit, offset)

    def update_task(self, task_id: uuid.UUID, user_id: uuid.UUID, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update a task with business logic validation.

        Args:
            task_id (uuid.UUID): ID of the task to update
            user_id (uuid.UUID): ID of the user (for authorization)
            task_data (TaskUpdate): Task update data

        Returns:
            Optional[Task]: The updated task if found and authorized, None otherwise
        """
        # Add any business logic validation here before updating the task

        return self.task_repo.update_task(task_id, user_id, task_data)

    def delete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """
        Delete a task with business logic validation.

        Args:
            task_id (uuid.UUID): ID of the task to delete
            user_id (uuid.UUID): ID of the user (for authorization)

        Returns:
            bool: True if task was deleted, False otherwise
        """
        # Add any business logic validation here before deleting the task

        return self.task_repo.delete_task(task_id, user_id)

    def complete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """
        Mark a task as completed with business logic validation.

        Args:
            task_id (uuid.UUID): ID of the task to complete
            user_id (uuid.UUID): ID of the user (for authorization)

        Returns:
            Optional[Task]: The updated task if found and authorized, None otherwise
        """
        # Add any business logic validation here before completing the task

        return self.task_repo.complete_task(task_id, user_id)