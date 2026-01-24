from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID
    tool_calls: list = []


class ConversationSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ConversationCreate(BaseModel):
    title: Optional[str] = None
    user_id: UUID