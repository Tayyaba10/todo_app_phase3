from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..models.message import Message, MessageCreate, SenderType


class MessageService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_message(self, message_data: MessageCreate) -> Message:
        """Create a new message."""
        message = Message.from_orm(message_data)
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def get_message_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get a message by its ID."""
        statement = select(Message).where(Message.id == message_id)
        return self.db_session.exec(statement).first()

    def get_messages_by_conversation(self, conversation_id: UUID) -> List[Message]:
        """Get all messages for a specific conversation, ordered by timestamp."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp)
        return self.db_session.exec(statement).all()

    def get_messages_by_sender(self, conversation_id: UUID, sender_type: SenderType) -> List[Message]:
        """Get all messages from a specific sender in a conversation."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.sender_type == sender_type
        ).order_by(Message.timestamp)
        return self.db_session.exec(statement).all()

    def update_message_content(self, message_id: UUID, content: str) -> Optional[Message]:
        """Update message content."""
        message = self.get_message_by_id(message_id)
        if message:
            message.content = content
            message.timestamp = datetime.utcnow()
            self.db_session.add(message)
            self.db_session.commit()
            self.db_session.refresh(message)
        return message

    def delete_message(self, message_id: UUID) -> bool:
        """Delete a message."""
        message = self.get_message_by_id(message_id)
        if message:
            self.db_session.delete(message)
            self.db_session.commit()
            return True
        return False

    def get_recent_messages(self, conversation_id: UUID, limit: int = 10) -> List[Message]:
        """Get the most recent messages from a conversation."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.desc()).limit(limit)
        messages = self.db_session.exec(statement).all()
        # Return in chronological order (oldest first)
        return list(reversed(messages))

    def count_messages_in_conversation(self, conversation_id: UUID) -> int:
        """Count the number of messages in a conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id)
        return len(self.db_session.exec(statement).all())