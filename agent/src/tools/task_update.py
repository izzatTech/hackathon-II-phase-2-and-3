"""
Task update MCP tool for the Todo application.
Provides functionality for AI agents to update tasks.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://backend:8000")


class TaskUpdateArgs(BaseModel):
    """Arguments for task update tool."""
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None


class TaskUpdateResult(BaseModel):
    """Result of task update tool."""
    success: bool
    task: Dict[str, Any] = None
    error: str = None


async def task_update_tool(args: TaskUpdateArgs, user_token: str) -> TaskUpdateResult:
    """
    Update an existing task via the backend API.

    Args:
        args (TaskUpdateArgs): Arguments for task update
        user_token (str): User's authentication token

    Returns:
        TaskUpdateResult: Result of the task update operation
    """
    try:
        # Validate required arguments
        if not args.task_id:
            return TaskUpdateResult(success=False, error="task_id is required")

        # Prepare the request payload with only provided fields
        payload = {}
        if args.title is not None:
            payload["title"] = args.title
        if args.description is not None:
            payload["description"] = args.description
        if args.status is not None:
            payload["status"] = args.status
        if args.priority is not None:
            payload["priority"] = args.priority
        if args.due_date is not None:
            payload["due_date"] = args.due_date

        # If no fields to update, return an error
        if not payload:
            return TaskUpdateResult(success=False, error="No fields provided to update")

        # Make the API request to update the task
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(
                f"{BACKEND_BASE_URL}/tasks/{args.task_id}",
                json=payload,
                headers={
                    "Authorization": f"Bearer {user_token}",
                    "Content-Type": "application/json"
                }
            )

        # Check if the request was successful
        if response.status_code == 200:
            # Task updated successfully
            task_data = response.json()
            return TaskUpdateResult(success=True, task=task_data)
        else:
            # Task update failed
            error_detail = response.json().get("detail", f"HTTP {response.status_code}")
            return TaskUpdateResult(success=False, error=f"Failed to update task: {error_detail}")

    except httpx.RequestError as e:
        # Network error occurred
        return TaskUpdateResult(success=False, error=f"Network error: {str(e)}")

    except Exception as e:
        # Other error occurred
        return TaskUpdateResult(success=False, error=f"Unexpected error: {str(e)}")