"""
Main AI agent for the Todo application.
Uses OpenAI SDK and MCP tools to process user requests and manage tasks.
"""

from typing import Dict, Any, Optional
import openai
import os
from dotenv import load_dotenv
from ..tools.task_create import TaskCreateArgs, task_create_tool
from ..tools.task_list import TaskListArgs, task_list_tool
from ..tools.task_update import TaskUpdateArgs, task_update_tool
from ..tools.task_delete import TaskDeleteArgs, task_delete_tool
from ..tools.task_complete import TaskCompleteArgs, task_complete_tool


# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


class TodoAgent:
    """
    AI agent that processes natural language requests and performs task operations
    using MCP-compliant tools.
    """

    def __init__(self):
        """Initialize the TodoAgent."""
        self.client = openai.OpenAI(api_key=openai.api_key)

    async def process_request(self, user_input: str, user_token: str) -> Dict[str, Any]:
        """
        Process a user's natural language request and return an appropriate response.

        Args:
            user_input (str): The user's natural language request
            user_token (str): The user's authentication token

        Returns:
            Dict[str, Any]: Response from the AI agent
        """
        # Define the available functions (tools) that the AI can call
        functions = [
            {
                "name": "task_create",
                "description": "Create a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Title of the task"},
                        "description": {"type": "string", "description": "Description of the task"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"], "description": "Priority of the task"},
                        "due_date": {"type": "string", "description": "Due date for the task in ISO format"}
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "task_list",
                "description": "List tasks for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status_filter": {"type": "string", "enum": ["pending", "in_progress", "completed"], "description": "Filter tasks by status"},
                        "priority_filter": {"type": "string", "enum": ["low", "medium", "high", "critical"], "description": "Filter tasks by priority"},
                        "limit": {"type": "integer", "description": "Number of tasks to return", "default": 50},
                        "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                    }
                }
            },
            {
                "name": "task_update",
                "description": "Update an existing task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to update"},
                        "title": {"type": "string", "description": "New title for the task"},
                        "description": {"type": "string", "description": "New description for the task"},
                        "status": {"type": "string", "enum": ["pending", "in_progress", "completed"], "description": "New status for the task"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"], "description": "New priority for the task"},
                        "due_date": {"type": "string", "description": "New due date for the task in ISO format"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "task_delete",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "task_complete",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to mark as completed"}
                    },
                    "required": ["task_id"]
                }
            }
        ]

        try:
            # Create a chat completion request with function calling
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or another supported model
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a helpful assistant that manages tasks for users.
                        Use the available functions to create, list, update, delete, or complete tasks.
                        When a user wants to create a task, extract the title, description, priority, and due date.
                        When a user wants to list tasks, decide if they want to filter by status or priority.
                        When a user wants to update a task, identify the task ID and the fields to update.
                        When a user wants to delete a task, identify the task ID.
                        When a user wants to complete a task, identify the task ID.
                        If you cannot determine the appropriate function, ask the user for clarification.
                        """
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                functions=functions,
                function_call="auto"  # Auto-determine which function to call
            )

            # Check if the model wants to call a function
            if response.choices[0].finish_reason == "function_call":
                # Extract function name and arguments
                function_call = response.choices[0].message.function_call
                function_name = function_call.name
                function_args = eval(function_call.arguments)  # Safe in controlled environment

                # Call the appropriate tool function
                if function_name == "task_create":
                    result = await task_create_tool(TaskCreateArgs(**function_args), user_token)
                elif function_name == "task_list":
                    result = await task_list_tool(TaskListArgs(**function_args), user_token)
                elif function_name == "task_update":
                    result = await task_update_tool(TaskUpdateArgs(**function_args), user_token)
                elif function_name == "task_delete":
                    result = await task_delete_tool(TaskDeleteArgs(**function_args), user_token)
                elif function_name == "task_complete":
                    result = await task_complete_tool(TaskCompleteArgs(**function_args), user_token)
                else:
                    return {"error": f"Unknown function: {function_name}"}

                if result.success:
                    return {"success": True, "result": result.dict()}
                else:
                    return {"success": False, "error": result.error}

            else:
                # The model returned a regular text response
                return {
                    "success": True,
                    "result": {
                        "message": response.choices[0].message.content
                    }
                }

        except openai.APIError as e:
            return {"success": False, "error": f"OpenAI API error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}