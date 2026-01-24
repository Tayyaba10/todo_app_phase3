from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class SenderType(str, Enum):
    user = "user"
    agent = "agent"


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    sender_type: SenderType = Field(sa_column_kwargs={"default": SenderType.user})
    content: str = Field(nullable=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    metadata_json: Optional[str] = Field(default=None)  # JSON string for tool calls, etc.

    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")


# Add schemas for API usage
class MessageCreate(SQLModel):
    conversation_id: UUID
    sender_type: SenderType
    content: str
    metadata_json: Optional[str] = None


class MessageRead(SQLModel):
    id: UUID
    conversation_id: UUID
    sender_type: SenderType
    content: str
    timestamp: datetime
    metadata_json: Optional[str]