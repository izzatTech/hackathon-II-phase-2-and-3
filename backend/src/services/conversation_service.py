"""
Conversation service for the Todo application.
Handles business logic for chat conversations and AI message processing.
"""

from typing import Dict, List, Optional
from sqlmodel import Session
from backend.src.models.conversation import Conversation, Message
from backend.src.repositories.conversation_repository import ConversationRepository
import uuid


class ConversationService:
    """Service class for handling conversation operations and AI message processing."""

    def __init__(self, session: Session, conversation_repo: ConversationRepository):
        """
        Initialize the ConversationService.

        Args:
            session (Session): Database session
            conversation_repo (ConversationRepository): Conversation repository
        """
        self.session = session
        self.conversation_repo = conversation_repo

    def create_conversation(self, user_id: uuid.UUID, title: Optional[str] = None) -> Optional[Conversation]:
        """
        Create a new conversation for a user.

        Args:
            user_id (uuid.UUID): ID of the user creating the conversation
            title (Optional[str]): Title for the conversation

        Returns:
            Optional[Conversation]: The created conversation if successful, None otherwise
        """
        return self.conversation_repo.create_conversation(user_id, title)

    def get_conversation_by_id(self, conversation_id: uuid.UUID) -> Optional[Conversation]:
        """
        Get a conversation by its ID.

        Args:
            conversation_id (uuid.UUID): ID of the conversation

        Returns:
            Optional[Conversation]: The conversation if found, None otherwise
        """
        return self.conversation_repo.get_conversation_by_id(conversation_id)

    def get_conversations_by_user(self, user_id: uuid.UUID) -> List[Conversation]:
        """
        Get all conversations for a specific user.

        Args:
            user_id (uuid.UUID): ID of the user

        Returns:
            List[Conversation]: List of conversations belonging to the user
        """
        return self.conversation_repo.get_conversations_by_user(user_id)

    def process_user_message(self, conversation_id: uuid.UUID, user_id: uuid.UUID, message_content: str) -> Optional[Dict]:
        """
        Process a user message and generate an AI response.

        Args:
            conversation_id (uuid.UUID): ID of the conversation
            user_id (uuid.UUID): ID of the user sending the message
            message_content (str): Content of the user message

        Returns:
            Optional[Dict]: Dictionary containing user message and AI response if successful, None otherwise
        """
        # First, save the user's message
        user_message = self.conversation_repo.create_message(
            conversation_id=conversation_id,
            sender_type="user",
            content=message_content
        )

        # For now, we'll simulate a simple AI response
        # In a real implementation, this would connect to the AI agent via MCP
        ai_response_content = self._generate_ai_response(message_content)

        # Save the AI's response
        ai_message = self.conversation_repo.create_message(
            conversation_id=conversation_id,
            sender_type="ai_assistant",
            content=ai_response_content
        )

        # Update the conversation's last activity time
        self.conversation_repo.update_conversation(conversation_id)

        return {
            "user_message": {
                "id": user_message.id,
                "content": user_message.content,
                "timestamp": user_message.created_at.isoformat()
            },
            "ai_response": {
                "id": ai_message.id,
                "content": ai_message.content,
                "timestamp": ai_message.created_at.isoformat()
            }
        }

    def _generate_ai_response(self, user_message: str) -> str:
        """
        Generate a simulated AI response based on the user's message.
        In a real implementation, this would connect to the AI agent via MCP.

        Args:
            user_message (str): The user's message

        Returns:
            str: AI response content
        """
        # Convert to lowercase for easier pattern matching
        lower_msg = user_message.lower()

        # Simple response patterns - this would be replaced by actual AI processing
        if any(word in lower_msg for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm your AI assistant. How can I help you manage your tasks today?"

        elif any(word in lower_msg for word in ['add', 'create', 'new', 'make']):
            if any(word in lower_msg for word in ['task', 'todo', 'item']):
                return "I can help you create a task. Please tell me the task title and any details you'd like to include."
            else:
                return "What would you like to add? I can help with tasks and reminders."

        elif any(word in lower_msg for word in ['list', 'show', 'see', 'view']):
            if any(word in lower_msg for word in ['task', 'tasks', 'todo']):
                return "I can show your tasks. Would you like to see all tasks, completed tasks, or pending tasks?"
            else:
                return "What would you like to see? I can help retrieve your tasks."

        elif any(word in lower_msg for word in ['complete', 'done', 'finish', 'finished']):
            return "I can help you mark tasks as complete. Could you tell me which task you've finished?"

        elif any(word in lower_msg for word in ['help', 'support', 'assist']):
            return "I'm here to help you manage your tasks! You can ask me to create, list, update, or complete tasks."

        elif any(word in lower_msg for word in ['thank', 'thanks', 'appreciate']):
            return "You're welcome! Is there anything else I can help you with?"

        else:
            return "I understand you said: '" + user_message + "'. How can I help you with your tasks?"

    def get_messages_for_conversation(self, conversation_id: uuid.UUID) -> List[Message]:
        """
        Get all messages for a specific conversation.

        Args:
            conversation_id (uuid.UUID): ID of the conversation

        Returns:
            List[Message]: List of messages in the conversation
        """
        return self.conversation_repo.get_messages_for_conversation(conversation_id)

    def get_recent_messages(self, conversation_id: uuid.UUID, limit: int = 10) -> List[Message]:
        """
        Get recent messages from a conversation.

        Args:
            conversation_id (uuid.UUID): ID of the conversation
            limit (int): Maximum number of messages to return

        Returns:
            List[Message]: List of recent messages
        """
        return self.conversation_repo.get_recent_messages(conversation_id, limit)

    def update_conversation_title(self, conversation_id: uuid.UUID, new_title: str) -> Optional[Conversation]:
        """
        Update the title of a conversation.

        Args:
            conversation_id (uuid.UUID): ID of the conversation
            new_title (str): New title for the conversation

        Returns:
            Optional[Conversation]: The updated conversation if found, None otherwise
        """
        return self.conversation_repo.update_conversation(conversation_id, title=new_title)

    def close_conversation(self, conversation_id: uuid.UUID) -> bool:
        """
        Close a conversation by setting its active status to False.

        Args:
            conversation_id (uuid.UUID): ID of the conversation

        Returns:
            bool: True if conversation was closed, False otherwise
        """
        conversation = self.conversation_repo.update_conversation(conversation_id, is_active=False)
        return conversation is not None