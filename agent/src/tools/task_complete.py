"""
Task complete MCP tool for the Todo application.
Provides functionality for AI agents to mark tasks as completed.
"""

from typing import Dict, Any
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://backend:8000")


class TaskCompleteArgs(BaseModel):
    """Arguments for task complete tool."""
    task_id: str


class TaskCompleteResult(BaseModel):
    """Result of task complete tool."""
    success: bool
    task: Dict[str, Any] = None
    error: str = None


async def task_complete_tool(args: TaskCompleteArgs, user_token: str) -> TaskCompleteResult:
    """
    Mark a task as completed via the backend API.

    Args:
        args (TaskCompleteArgs): Arguments for task completion
        user_token (str): User's authentication token

    Returns:
        TaskCompleteResult: Result of the task completion operation
    """
    try:
        # Validate required arguments
        if not args.task_id:
            return TaskCompleteResult(success=False, error="task_id is required")

        # Make the API request to mark the task as completed
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.patch(
                f"{BACKEND_BASE_URL}/tasks/{args.task_id}/complete",
                headers={
                    "Authorization": f"Bearer {user_token}",
                    "Content-Type": "application/json"
                }
            )

        # Check if the request was successful
        if response.status_code == 200:
            # Task marked as completed successfully
            task_data = response.json()
            return TaskCompleteResult(success=True, task=task_data)
        else:
            # Task completion failed
            error_detail = response.json().get("detail", f"HTTP {response.status_code}")
            return TaskCompleteResult(success=False, error=f"Failed to complete task: {error_detail}")

    except httpx.RequestError as e:
        # Network error occurred
        return TaskCompleteResult(success=False, error=f"Network error: {str(e)}")

    except Exception as e:
        # Other error occurred
        return TaskCompleteResult(success=False, error=f"Unexpected error: {str(e)}")