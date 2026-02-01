from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class RegisterResponse(BaseModel):
    user_id: UUID
    email: str
    name: Optional[str]
    created_at: datetime
    token: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    user_id: UUID
    email: str
    name: Optional[str]
    token: str


class ProfileResponse(BaseModel):
    id: UUID
    email: str
    name: Optional[str]
    created_at: datetime
    updated_at: datetime