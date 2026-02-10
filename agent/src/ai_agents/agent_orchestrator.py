"""
Agent orchestrator for the Todo application.
Manages the interaction between the AI agent and the MCP tools.
"""

from typing import Dict, Any
from ..ai_agents.main_agent import TodoAgent
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrator that manages communication between the frontend/MCP server
    and the AI agent, ensuring proper tool usage and response handling.
    """

    def __init__(self):
        """Initialize the AgentOrchestrator."""
        self.agent = TodoAgent()

    async def process_user_request(self, user_input: str, user_token: str) -> Dict[str, Any]:
        """
        Process a user's natural language request through the AI agent.

        Args:
            user_input (str): The user's natural language request
            user_token (str): The user's authentication token

        Returns:
            Dict[str, Any]: The response from the AI agent
        """
        logger.info(f"Processing user request: {user_input}")

        # Pass the request to the AI agent
        result = await self.agent.process_request(user_input, user_token)

        logger.info(f"AI agent result: {result}")
        return result

    async def execute_tool(self, tool_name: str, tool_args: Dict[str, Any], user_token: str) -> Dict[str, Any]:
        """
        Execute a specific tool with the given arguments.

        Args:
            tool_name (str): Name of the tool to execute
            tool_args (Dict[str, Any]): Arguments for the tool
            user_token (str): The user's authentication token

        Returns:
            Dict[str, Any]: Result of the tool execution
        """
        logger.info(f"Executing tool '{tool_name}' with args: {tool_args}")

        # In a real implementation, this would route to the appropriate tool
        # For now, we'll simulate by using the AI agent's processing capability
        # which already handles various tools based on the input
        mock_input = f"Please execute {tool_name} with arguments: {tool_args}"

        # Pass to the agent with special instructions to execute the tool directly
        result = await self.agent.process_request(mock_input, user_token)

        logger.info(f"Tool execution result: {result}")
        return result

    async def handle_conversation_turn(self, user_message: str, conversation_context: Dict[str, Any], user_token: str) -> Dict[str, Any]:
        """
        Handle a single turn in a conversation with the AI agent.

        Args:
            user_message (str): The user's message
            conversation_context (Dict[str, Any]): Context of the current conversation
            user_token (str): The user's authentication token

        Returns:
            Dict[str, Any]: Response to the user's message
        """
        logger.info(f"Handling conversation turn with message: {user_message}")

        # Process the user's message
        result = await self.process_user_request(user_message, user_token)

        # Return the response with additional context if needed
        response = {
            "response": result,
            "conversation_id": conversation_context.get("conversation_id"),
            "timestamp": conversation_context.get("timestamp")
        }

        logger.info(f"Conversation turn response: {response}")
        return response

    def validate_user_token(self, user_token: str) -> bool:
        """
        Validate a user's authentication token.

        Args:
            user_token (str): The user's authentication token

        Returns:
            bool: True if the token is valid, False otherwise
        """
        # In a real implementation, this would call an authentication service
        # to validate the token. For now, we'll just check if it's non-empty.
        is_valid = bool(user_token and user_token.strip())
        logger.info(f"Token validation result: {is_valid}")
        return is_valid