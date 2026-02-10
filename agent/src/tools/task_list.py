"""
Task list MCP tool for the Todo application.
Provides functionality for AI agents to list tasks.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://backend:8000")


class TaskListArgs(BaseModel):
    """Arguments for task list tool."""
    status_filter: Optional[str] = None
    priority_filter: Optional[str] = None
    limit: int = 50
    offset: int = 0


class TaskListResult(BaseModel):
    """Result of task list tool."""
    success: bool
    tasks: list = []
    total_count: int = 0
    error: str = None


async def task_list_tool(args: TaskListArgs, user_token: str) -> TaskListResult:
    """
    List tasks for the current user via the backend API.

    Args:
        args (TaskListArgs): Arguments for task listing
        user_token (str): User's authentication token

    Returns:
        TaskListResult: Result of the task listing operation
    """
    try:
        # Prepare the query parameters
        params = {
            "limit": args.limit,
            "offset": args.offset
        }

        if args.status_filter:
            params["status_filter"] = args.status_filter

        if args.priority_filter:
            params["priority_filter"] = args.priority_filter

        # Make the API request to list tasks
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BACKEND_BASE_URL}/tasks/",
                params=params,
                headers={
                    "Authorization": f"Bearer {user_token}",
                    "Content-Type": "application/json"
                }
            )

        # Check if the request was successful
        if response.status_code == 200:
            # Tasks retrieved successfully
            response_data = response.json()
            return TaskListResult(
                success=True,
                tasks=response_data,
                total_count=len(response_data)
            )
        else:
            # Task listing failed
            error_detail = response.json().get("detail", f"HTTP {response.status_code}")
            return TaskListResult(success=False, error=f"Failed to list tasks: {error_detail}")

    except httpx.RequestError as e:
        # Network error occurred
        return TaskListResult(success=False, error=f"Network error: {str(e)}")

    except Exception as e:
        # Other error occurred
        return TaskListResult(success=False, error=f"Unexpected error: {str(e)}")