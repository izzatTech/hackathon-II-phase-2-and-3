"""
Task API endpoints for the Todo application.
Provides endpoints for task creation, retrieval, updating, and deletion.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from backend.src.models.task import Task
from backend.src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from backend.src.repositories.task_repository import TaskRepository
from backend.src.middleware.auth import require_authentication
from backend.src.config.database import get_session
import uuid


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Get tasks for the current authenticated user with optional filtering.

    Args:
        status_filter (Optional[str]): Filter tasks by status
        priority_filter (Optional[str]): Filter tasks by priority
        limit (int): Maximum number of tasks to return (default: 50)
        offset (int): Offset for pagination (default: 0)
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        List[TaskResponse]: List of tasks matching the criteria
    """
    task_repo = TaskRepository(db)

    tasks = task_repo.get_tasks_by_user(
        user_id=uuid.UUID(current_user_id),
        status=status_filter,
        priority=priority_filter,
        limit=limit,
        offset=offset
    )

    return [TaskResponse.from_orm(task) for task in tasks]


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Create a new task for the current authenticated user.

    Args:
        task_data (TaskCreate): Task creation data
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        TaskResponse: The created task information
    """
    task_repo = TaskRepository(db)

    task = task_repo.create_task(
        task_data=task_data,
        user_id=uuid.UUID(current_user_id)
    )

    return TaskResponse.from_orm(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the current authenticated user.

    Args:
        task_id (str): ID of the task to retrieve
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        TaskResponse: The requested task information

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    task_repo = TaskRepository(db)

    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = task_repo.get_task_by_id(
        task_id=task_uuid,
        user_id=uuid.UUID(current_user_id)
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return TaskResponse.from_orm(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the current authenticated user.

    Args:
        task_id (str): ID of the task to update
        task_data (TaskUpdate): Task update data
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        TaskResponse: The updated task information

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    task_repo = TaskRepository(db)

    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = task_repo.update_task(
        task_id=task_uuid,
        user_id=uuid.UUID(current_user_id),
        task_data=task_data
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return TaskResponse.from_orm(task)


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the current authenticated user.

    Args:
        task_id (str): ID of the task to delete
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    task_repo = TaskRepository(db)

    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    success = task_repo.delete_task(
        task_id=task_uuid,
        user_id=uuid.UUID(current_user_id)
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return {"message": "Task successfully deleted"}


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: str,
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Mark a specific task as completed for the current authenticated user.

    Args:
        task_id (str): ID of the task to mark as completed
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        TaskResponse: The updated task information

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    task_repo = TaskRepository(db)

    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = task_repo.complete_task(
        task_id=task_uuid,
        user_id=uuid.UUID(current_user_id)
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or doesn't belong to user"
        )

    return TaskResponse.from_orm(task)