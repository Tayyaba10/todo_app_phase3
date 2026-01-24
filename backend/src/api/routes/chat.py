from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import Optional
from sqlmodel import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...database import get_session
from ...services.agent_service import AgentService
from ...api.deps import get_current_user
from ...api.schemas.conversation import ChatRequest, ChatResponse
import os
import logging


# Set up logging
logger = logging.getLogger(__name__)

# Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

# Initialize router
router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
def chat(
    user_id: UUID,
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Process a chat message through the AI agent.
    """
    logger.info(f"Received chat request for user {user_id}, conversation {chat_request.conversation_id}")

    # Verify that the user_id in the path matches the authenticated user
    if str(current_user["user_id"]) != str(user_id):
        logger.warning(f"Access denied: user {current_user['user_id']} tried to access {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's chat"
        )

    # Get OpenAI API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error("OpenAI API key not configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI API key not configured"
        )

    # Initialize agent service
    agent_service = AgentService(db_session=db, openai_api_key=openai_api_key)

    try:
        # Process the message through the agent
        result = agent_service.process_user_message(
            user_id=user_id,
            message_content=chat_request.message,
            conversation_id=chat_request.conversation_id
        )
        logger.info(f"Successfully processed message for user {user_id}, conversation {result['conversation_id']}")
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error processing message for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


# Health check endpoint
@router.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "service": "chat-api"}