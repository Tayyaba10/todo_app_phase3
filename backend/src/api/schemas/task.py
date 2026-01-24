from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Request schemas
class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskToggleCompleteRequest(BaseModel):
    completed: bool


# Response schemas
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]


class MessageResponse(BaseModel):
    message: str