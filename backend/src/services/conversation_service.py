from sqlmodel import Session, select, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate


class ConversationService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=conversation_data.user_id,
            title=conversation_data.title
        )
        self.db_session.add(conversation)
        self.db_session.commit()
        self.db_session.refresh(conversation)
        return conversation

    def add_message_to_conversation(self, message_data: MessageCreate) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=message_data.conversation_id,
            sender_type=message_data.sender_type,
            content=message_data.content,
            metadata_json=message_data.metadata_json
        )
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def save_user_message(self, conversation_id: UUID, content: str, metadata_json: Optional[str] = None) -> Message:
        """Save a user message to the conversation."""
        message_data = MessageCreate(
            conversation_id=conversation_id,
            sender_type="user",  # Using string instead of enum to avoid circular imports
            content=content,
            metadata_json=metadata_json
        )
        return self.add_message_to_conversation(message_data)

    def save_agent_message(self, conversation_id: UUID, content: str, metadata_json: Optional[str] = None) -> Message:
        """Save an agent message to the conversation."""
        message_data = MessageCreate(
            conversation_id=conversation_id,
            sender_type="agent",  # Using string instead of enum to avoid circular imports
            content=content,
            metadata_json=metadata_json
        )
        return self.add_message_to_conversation(message_data)

    def get_conversation_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by its ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return self.db_session.exec(statement).first()

    def get_conversation_by_id_with_messages(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by its ID with all associated messages."""
        statement = select(Conversation).where(Conversation.id == conversation_id).options(joinedload(Conversation.messages))
        return self.db_session.exec(statement).first()

    def get_conversations_by_user(self, user_id: UUID) -> List[Conversation]:
        """Get all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return self.db_session.exec(statement).all()

    def get_conversation_with_messages(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation with all its messages."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = self.db_session.exec(statement).first()
        if conversation:
            # Load messages as well
            conversation.messages = self.get_messages_for_conversation(conversation_id)
        return conversation

    def get_messages_for_conversation(self, conversation_id: UUID) -> List[Message]:
        """Get all messages for a specific conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        return self.db_session.exec(statement).all()

    def get_conversation_history(self, conversation_id: UUID, limit: int = 50) -> List[Message]:
        """Get conversation history with a limit for context."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.desc()).limit(limit)
        messages = self.db_session.exec(statement).all()
        # Return in chronological order (oldest first)
        return list(reversed(messages))

    def get_recent_conversations(self, user_id: UUID, limit: int = 10) -> List[Conversation]:
        """Get recent conversations for a user."""
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).limit(limit)
        return self.db_session.exec(statement).all()

    def update_conversation_title(self, conversation_id: UUID, title: str) -> Optional[Conversation]:
        """Update conversation title."""
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.title = title
            from datetime import datetime
            conversation.updated_at = datetime.utcnow()
            self.db_session.add(conversation)
            self.db_session.commit()
            self.db_session.refresh(conversation)
        return conversation

    def deactivate_conversation(self, conversation_id: UUID) -> bool:
        """Deactivate a conversation."""
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.is_active = False
            self.db_session.add(conversation)
            self.db_session.commit()
            return True
        return False