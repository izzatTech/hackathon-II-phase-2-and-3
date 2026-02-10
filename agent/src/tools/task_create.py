"""
Task creation MCP tool for the Todo application.
Provides functionality for AI agents to create tasks.
"""

from typing import Dict, Any
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://backend:8000")


class TaskCreateArgs(BaseModel):
    """Arguments for task creation tool."""
    title: str
    description: str = None
    priority: str = "medium"
    due_date: str = None


class TaskCreateResult(BaseModel):
    """Result of task creation tool."""
    success: bool
    task: Dict[str, Any] = None
    error: str = None


async def task_create_tool(args: TaskCreateArgs, user_token: str) -> TaskCreateResult:
    """
    Create a new task via the backend API.

    Args:
        args (TaskCreateArgs): Arguments for task creation
        user_token (str): User's authentication token

    Returns:
        TaskCreateResult: Result of the task creation operation
    """
    try:
        # Prepare the request payload
        payload = {
            "title": args.title,
            "description": args.description,
            "priority": args.priority
        }

        if args.due_date:
            payload["due_date"] = args.due_date

        # Make the API request to create the task
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{BACKEND_BASE_URL}/tasks/",
                json=payload,
                headers={
                    "Authorization": f"Bearer {user_token}",
                    "Content-Type": "application/json"
                }
            )

        # Check if the request was successful
        if response.status_code == 201:
            # Task created successfully
            task_data = response.json()
            return TaskCreateResult(success=True, task=task_data)
        else:
            # Task creation failed
            error_detail = response.json().get("detail", f"HTTP {response.status_code}")
            return TaskCreateResult(success=False, error=f"Failed to create task: {error_detail}")

    except httpx.RequestError as e:
        # Network error occurred
        return TaskCreateResult(success=False, error=f"Network error: {str(e)}")

    except Exception as e:
        # Other error occurred
        return TaskCreateResult(success=False, error=f"Unexpected error: {str(e)}")