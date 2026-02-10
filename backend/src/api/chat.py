"""
Chat API endpoints for the Todo application.
Provides endpoints for AI-powered chat and task management through natural language.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from backend.src.models.user import User
from backend.src.models.conversation import Conversation, Message
from backend.src.repositories.conversation_repository import ConversationRepository
from backend.src.services.conversation_service import ConversationService
from backend.src.middleware.auth import require_authentication
from backend.src.config.database import get_session
import uuid


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/conversations")
def create_conversation(
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Create a new conversation for the current user.

    Args:
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        dict: The created conversation information
    """
    conversation_repo = ConversationRepository(db)
    conversation_service = ConversationService(db, conversation_repo)

    conversation = conversation_service.create_conversation(uuid.UUID(current_user_id))

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation"
        )

    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at
    }


@router.get("/conversations")
def get_user_conversations(
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Get all conversations for the current user.

    Args:
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        List[dict]: List of user's conversations
    """
    conversation_repo = ConversationRepository(db)
    conversation_service = ConversationService(db, conversation_repo)

    conversations = conversation_service.get_conversations_by_user(uuid.UUID(current_user_id))

    return [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at
        }
        for conv in conversations
    ]


@router.post("/conversations/{conversation_id}/messages")
def send_message(
    conversation_id: str,
    message_content: str,
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Send a message in a conversation and get AI response.

    Args:
        conversation_id (str): ID of the conversation
        message_content (str): Content of the message
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        dict: The sent message and AI response
    """
    conversation_repo = ConversationRepository(db)
    conversation_service = ConversationService(db, conversation_repo)

    try:
        conv_uuid = uuid.UUID(conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )

    # Verify the user has access to this conversation
    conversation = conversation_service.get_conversation_by_id(conv_uuid)
    if not conversation or str(conversation.user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Process the message and get AI response
    result = conversation_service.process_user_message(
        conversation_id=conv_uuid,
        user_id=uuid.UUID(current_user_id),
        message_content=message_content
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message"
        )

    return result


@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: str,
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Get all messages in a specific conversation.

    Args:
        conversation_id (str): ID of the conversation
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        List[dict]: List of messages in the conversation
    """
    conversation_repo = ConversationRepository(db)
    conversation_service = ConversationService(db, conversation_repo)

    try:
        conv_uuid = uuid.UUID(conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )

    # Verify the user has access to this conversation
    conversation = conversation_service.get_conversation_by_id(conv_uuid)
    if not conversation or str(conversation.user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    messages = conversation_service.get_messages_for_conversation(conv_uuid)

    return [
        {
            "id": msg.id,
            "sender_type": msg.sender_type,
            "content": msg.content,
            "created_at": msg.created_at,
        }
        for msg in messages
    ]