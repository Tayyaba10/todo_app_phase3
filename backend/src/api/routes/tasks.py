from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..deps import get_current_user
from ..schemas.task import TaskCreateRequest, TaskResponse, TaskListResponse, TaskUpdateRequest, TaskToggleCompleteRequest, MessageResponse
from ...services.task_service import TaskService
from ...models.task import Task
from ...core.database import get_session
from ...core.exceptions import TaskNotFoundException, InsufficientPermissionException


router = APIRouter()


@router.get("/", response_model=TaskListResponse)
def list_tasks(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    user_id = current_user["user_id"]

    tasks = TaskService.get_tasks_by_user(session=session, user_id=user_id)

    task_responses = [
        TaskResponse(
            id=task["id"],
            title=task["title"],
            description=task["description"],
            completed=task["completed"],
            user_id=task["user_id"],
            created_at=task["created_at"],
            updated_at=task["updated_at"]
        )
        for task in tasks
    ]

    return TaskListResponse(tasks=task_responses)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    user_id = current_user["user_id"]

    # Create the task using the service
    db_task = TaskService.create_task(
        session=session,
        task_create=task_create,
        user_id=user_id
    )

    # Return the created task
    return TaskResponse(
        id=db_task["id"],
        title=db_task["title"],
        description=db_task["description"],
        completed=db_task["completed"],
        user_id=db_task["user_id"],
        created_at=db_task["created_at"],
        updated_at=db_task["updated_at"]
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    user_id = current_user["user_id"]

    db_task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    return TaskResponse(
        id=db_task["id"],
        title=db_task["title"],
        description=db_task["description"],
        completed=db_task["completed"],
        user_id=db_task["user_id"],
        created_at=db_task["created_at"],
        updated_at=db_task["updated_at"]
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_update: TaskUpdateRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    user_id = current_user["user_id"]

    db_task = TaskService.update_task(
        session=session,
        task_id=task_id,
        task_update=task_update,
        user_id=user_id
    )

    return TaskResponse(
        id=db_task["id"],
        title=db_task["title"],
        description=db_task["description"],
        completed=db_task["completed"],
        user_id=db_task["user_id"],
        created_at=db_task["created_at"],
        updated_at=db_task["updated_at"]
    )


@router.delete("/{task_id}", response_model=MessageResponse)
def delete_task(
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    user_id = current_user["user_id"]

    success = TaskService.delete_task(session=session, task_id=task_id, user_id=user_id)

    if success:
        return MessageResponse(message="Task deleted successfully")
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    task_id: UUID,
    task_toggle: TaskToggleCompleteRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user.
    """
    user_id = current_user["user_id"]

    db_task = TaskService.toggle_task_completion(session=session, task_id=task_id, user_id=user_id)

    return TaskResponse(
        id=db_task["id"],
        title=db_task["title"],
        description=db_task["description"],
        completed=db_task["completed"],
        user_id=db_task["user_id"],
        created_at=db_task["created_at"],
        updated_at=db_task["updated_at"]
    )