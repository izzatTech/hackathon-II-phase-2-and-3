"""
MCP (Model Context Protocol) server for the Todo application.
Exposes tools for AI agents to interact with the task management system.
"""

import asyncio
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os


# Pydantic models for request/response
class ToolCall(BaseModel):
    """Model representing a tool call."""
    name: str
    arguments: Dict[str, Any]


class ToolResponse(BaseModel):
    """Model representing a tool response."""
    success: bool
    result: Dict[str, Any] = {}
    error: str = None


# Initialize FastAPI app
app = FastAPI(
    title="Todo Application MCP Server",
    description="MCP server for AI agents to interact with the Todo application",
    version="1.0.0"
)


@app.get("/v1/tools")
async def list_tools():
    """Return a list of available tools and their schemas."""
    tools = [
        {
            "name": "task.create",
            "description": "Create a new task",
            "input_schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the task"},
                    "description": {"type": "string", "description": "Description of the task"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "medium"},
                    "due_date": {"type": "string", "format": "date-time", "description": "Due date for the task"}
                },
                "required": ["title"]
            }
        },
        {
            "name": "task.list",
            "description": "List tasks for the current user",
            "input_schema": {
                "type": "object",
                "properties": {
                    "status_filter": {"type": "string", "enum": ["pending", "in_progress", "completed"]},
                    "priority_filter": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 50},
                    "offset": {"type": "integer", "minimum": 0, "default": 0}
                }
            }
        },
        {
            "name": "task.update",
            "description": "Update an existing task",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to update"},
                    "updates": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "status": {"type": "string", "enum": ["pending", "in_progress", "completed"]},
                            "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                            "due_date": {"type": "string", "format": "date-time"}
                        }
                    }
                },
                "required": ["task_id", "updates"]
            }
        },
        {
            "name": "task.delete",
            "description": "Delete a task",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to delete"}
                },
                "required": ["task_id"]
            }
        },
        {
            "name": "task.complete",
            "description": "Mark a task as completed",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to complete"}
                },
                "required": ["task_id"]
            }
        }
    ]

    return {"tools": tools}


@app.post("/v1/tools/{tool_name}/call")
async def call_tool(tool_name: str, call: ToolCall):
    """Execute a tool call."""
    # In a real implementation, this would call the actual backend services
    # For now, we'll simulate the behavior

    try:
        if tool_name == "task.create":
            return await simulate_task_create(call.arguments)
        elif tool_name == "task.list":
            return await simulate_task_list(call.arguments)
        elif tool_name == "task.update":
            return await simulate_task_update(call.arguments)
        elif tool_name == "task.delete":
            return await simulate_task_delete(call.arguments)
        elif tool_name == "task.complete":
            return await simulate_task_complete(call.arguments)
        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


async def simulate_task_create(args: Dict[str, Any]) -> ToolResponse:
    """Simulate creating a task."""
    # In a real implementation, this would call the backend API
    import uuid
    from datetime import datetime

    task = {
        "id": str(uuid.uuid4()),
        "title": args.get("title"),
        "description": args.get("description"),
        "status": "pending",
        "priority": args.get("priority", "medium"),
        "due_date": args.get("due_date"),
        "created_at": datetime.utcnow().isoformat()
    }

    return ToolResponse(success=True, result={"task": task})


async def simulate_task_list(args: Dict[str, Any]) -> ToolResponse:
    """Simulate listing tasks."""
    # In a real implementation, this would call the backend API
    # For now, return sample tasks

    # Sample tasks for simulation
    sample_tasks = [
        {
            "id": "1",
            "title": "Sample Task 1",
            "description": "This is a sample task",
            "status": "pending",
            "priority": "medium",
            "due_date": None,
            "created_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "2",
            "title": "Sample Task 2",
            "description": "This is another sample task",
            "status": "completed",
            "priority": "high",
            "due_date": "2023-12-31T23:59:59Z",
            "created_at": "2023-01-02T00:00:00Z"
        }
    ]

    # Apply filters if provided
    status_filter = args.get("status_filter")
    priority_filter = args.get("priority_filter")

    filtered_tasks = sample_tasks
    if status_filter:
        filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]
    if priority_filter:
        filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]

    # Apply limits
    limit = args.get("limit", 50)
    offset = args.get("offset", 0)
    paginated_tasks = filtered_tasks[offset:offset + limit]

    return ToolResponse(success=True, result={"tasks": paginated_tasks, "total_count": len(filtered_tasks)})


async def simulate_task_update(args: Dict[str, Any]) -> ToolResponse:
    """Simulate updating a task."""
    # In a real implementation, this would call the backend API
    task_id = args.get("task_id")
    updates = args.get("updates", {})

    if not task_id:
        raise ValueError("task_id is required for update")

    # Simulate the updated task
    updated_task = {
        "id": task_id,
        "title": updates.get("title", "Updated Sample Task"),
        "description": updates.get("description", "Updated description"),
        "status": updates.get("status", "pending"),
        "priority": updates.get("priority", "medium"),
        "due_date": updates.get("due_date"),
        "created_at": "2023-01-01T00:00:00Z"
    }

    return ToolResponse(success=True, result={"task": updated_task})


async def simulate_task_delete(args: Dict[str, Any]) -> ToolResponse:
    """Simulate deleting a task."""
    task_id = args.get("task_id")

    if not task_id:
        raise ValueError("task_id is required for delete")

    # In a real implementation, this would call the backend API
    return ToolResponse(success=True, result={"message": f"Task {task_id} deleted successfully"})


async def simulate_task_complete(args: Dict[str, Any]) -> ToolResponse:
    """Simulate completing a task."""
    task_id = args.get("task_id")

    if not task_id:
        raise ValueError("task_id is required for complete")

    # Simulate the completed task
    completed_task = {
        "id": task_id,
        "title": "Sample Task",
        "description": "Sample description",
        "status": "completed",
        "priority": "medium",
        "due_date": None,
        "created_at": "2023-01-01T00:00:00Z"
    }

    return ToolResponse(success=True, result={"task": completed_task})


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "MCP Server"}


# Main entry point
if __name__ == "__main__":
    uvicorn.run(
        "mcp_server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True
    )