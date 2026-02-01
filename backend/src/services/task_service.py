from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import datetime
from ..models.task import Task, TaskCreate, TaskUpdate, TaskToggleComplete
from ..models.user import User
from ..core.exceptions import TaskNotFoundException, InsufficientPermissionException, UserNotFoundException


class TaskService:
    """
    Service class to handle task-related business logic.
    """

    @staticmethod
    def create_task(session: Session, task_create: 'TaskCreateRequest', user_id: UUID) -> dict:
        """
        Create a new task for the given user.
        """
        # Create a new task instance with the provided data and user_id
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Return a dictionary representation of the created task
        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at
        }

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID, user_id: UUID) -> Optional[dict]:
        """
        Get a specific task by ID for the given user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundException(task_id)

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": str(task.user_id),
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: UUID) -> List[dict]:
        """
        Get all tasks for the given user.
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        return [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": str(task.user_id),
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            for task in tasks
        ]

    @staticmethod
    def update_task(session: Session, task_id: UUID, task_update: 'TaskUpdateRequest', user_id: UUID = None) -> Optional[dict]:
        """
        Update a specific task for the given user.
        """
        statement = select(Task).where(Task.id == task_id)
        if user_id:
            statement = statement.where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        # Update only the fields that are provided
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.completed is not None:
            db_task.completed = task_update.completed

        db_task.updated_at = datetime.datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at
        }

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
        """
        Delete a specific task.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        session.delete(db_task)
        session.commit()

        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: UUID, user_id: UUID) -> Optional[dict]:
        """
        Toggle the completion status of a specific task for the given user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        # Toggle the completion status
        db_task.completed = not db_task.completed

        db_task.updated_at = datetime.datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at
        }