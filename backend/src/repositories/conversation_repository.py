"""
Conversation repository for the Todo application.
Handles all database operations for Conversation and Message entities.
"""

from typing import List, Optional
from sqlmodel import Session, select
from backend.src.models.conversation import Conversation, Message
import uuid


class ConversationRepository:
    """Repository class for handling Conversation and Message database operations."""

    def __init__(self, session: Session):
        """
        Initialize the ConversationRepository.

        Args:
            session (Session): Database session
        """
        self.session = session

    def create_conversation(self, user_id: uuid.UUID, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation.

        Args:
            user_id (uuid.UUID): ID of the user creating the conversation
            title (Optional[str]): Title for the conversation

        Returns:
            Conversation: The created conversation
        """
        from datetime import datetime
        conversation = Conversation(
            user_id=user_id,
            title=title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: uuid.UUID) -> Optional[Conversation]:
        """
        Get a conversation by its ID.

        Args:
            conversation_id (uuid.UUID): ID of the conversation

        Returns:
            Optional[Conversation]: The conversation if found, None otherwise
        """
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return self.session.exec(statement).first()

    def get_conversations_by_user(self, user_id: uuid.UUID) -> List[Conversation]:
        """
        Get all conversations for a specific user.

        Args:
            user_id (uuid.UUID): ID of the user

        Returns:
            List[Conversation]: List of conversations belonging to the user
        """
        statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        return self.session.exec(statement).all()

    def update_conversation(self, conversation_id: uuid.UUID, title: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[Conversation]:
        """
        Update a conversation.

        Args:
            conversation_id (uuid.UUID): ID of the conversation to update
            title (Optional[str]): New title for the conversation
            is_active (Optional[bool]): New active status for the conversation

        Returns:
            Optional[Conversation]: The updated conversation if found, None otherwise
        """
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None

        if title is not None:
            conversation.title = title
        if is_active is not None:
            conversation.is_active = is_active

        from datetime import datetime
        conversation.updated_at = datetime.utcnow()

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: uuid.UUID) -> bool:
        """
        Delete a conversation and all its messages.

        Args:
            conversation_id (uuid.UUID): ID of the conversation to delete

        Returns:
            bool: True if conversation was deleted, False otherwise
        """
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return False

        self.session.delete(conversation)
        self.session.commit()
        return True

    def create_message(self, conversation_id: uuid.UUID, sender_type: str, content: str, metadata: Optional[dict] = None) -> Message:
        """
        Create a new message in a conversation.

        Args:
            conversation_id (uuid.UUID): ID of the conversation
            sender_type (str): Type of sender ('user', 'ai_assistant', or 'system')
            content (str): Content of the message
            metadata (Optional[dict]): Additional metadata for the message

        Returns:
            Message: The created message
        """
        message = Message(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content,
            metadata_json=str(metadata) if metadata else None
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_messages_for_conversation(self, conversation_id: uuid.UUID) -> List[Message]:
        """
        Get all messages for a specific conversation.

        Args:
            conversation_id (uuid.UUID): ID of the conversation

        Returns:
            List[Message]: List of messages in the conversation
        """
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        return self.session.exec(statement).all()

    def get_recent_messages(self, conversation_id: uuid.UUID, limit: int = 10) -> List[Message]:
        """
        Get recent messages from a conversation.

        Args:
            conversation_id (uuid.UUID): ID of the conversation
            limit (int): Maximum number of messages to return

        Returns:
            List[Message]: List of recent messages
        """
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.desc()).limit(limit)
        messages = self.session.exec(statement).all()
        return list(reversed(messages))  # Reverse to get chronological order