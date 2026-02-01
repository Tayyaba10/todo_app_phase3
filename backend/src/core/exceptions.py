from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID


class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


class InsufficientPermissionException(HTTPException):
    def __init__(self, detail: Optional[str] = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )


class InvalidTokenException(HTTPException):
    def __init__(self, detail: Optional[str] = "Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )