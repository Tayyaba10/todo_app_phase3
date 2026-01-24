from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from datetime import datetime
from typing import Optional


class SenderType(str, Enum):
    user = "user"
    agent = "agent"


class MessageSchema(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_type: SenderType
    content: str
    timestamp: datetime
    metadata_json: Optional[str] = None


class MessageCreate(BaseModel):
    conversation_id: UUID
    sender_type: SenderType
    content: str
    metadata_json: Optional[str] = None


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    metadata_json: Optional[str] = None