"""
Task delete MCP tool for the Todo application.
Provides functionality for AI agents to delete tasks.
"""

from typing import Dict, Any
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://backend:8000")


class TaskDeleteArgs(BaseModel):
    """Arguments for task delete tool."""
    task_id: str


class TaskDeleteResult(BaseModel):
    """Result of task delete tool."""
    success: bool
    message: str = None
    error: str = None


async def task_delete_tool(args: TaskDeleteArgs, user_token: str) -> TaskDeleteResult:
    """
    Delete a task via the backend API.

    Args:
        args (TaskDeleteArgs): Arguments for task deletion
        user_token (str): User's authentication token

    Returns:
        TaskDeleteResult: Result of the task deletion operation
    """
    try:
        # Validate required arguments
        if not args.task_id:
            return TaskDeleteResult(success=False, error="task_id is required")

        # Make the API request to delete the task
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(
                f"{BACKEND_BASE_URL}/tasks/{args.task_id}",
                headers={
                    "Authorization": f"Bearer {user_token}",
                    "Content-Type": "application/json"
                }
            )

        # Check if the request was successful
        if response.status_code == 200:
            # Task deleted successfully
            response_data = response.json()
            return TaskDeleteResult(success=True, message=response_data.get("message", "Task deleted successfully"))
        else:
            # Task deletion failed
            error_detail = response.json().get("detail", f"HTTP {response.status_code}")
            return TaskDeleteResult(success=False, error=f"Failed to delete task: {error_detail}")

    except httpx.RequestError as e:
        # Network error occurred
        return TaskDeleteResult(success=False, error=f"Network error: {str(e)}")

    except Exception as e:
        # Other error occurred
        return TaskDeleteResult(success=False, error=f"Unexpected error: {str(e)}")