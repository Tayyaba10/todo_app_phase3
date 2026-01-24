from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate, TaskToggleComplete
from ..models.user import User
from ..core.exceptions import TaskNotFoundException, InsufficientPermissionException, UserNotFoundException


class TaskService:
    """
    Service class to handle task-related business logic.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_task(self, user_id: UUID, **kwargs) -> dict:
        """
        Create a new task for the given user.
        """
        # Create a new task instance with the provided data and user_id
        db_task = Task(
            title=kwargs.get('title'),
            description=kwargs.get('description', ''),
            completed=kwargs.get('completed', False),
            user_id=user_id
        )

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        # Return a dictionary representation of the created task
        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at.isoformat(),
            "updated_at": db_task.updated_at.isoformat()
        }

    def get_task_by_id(self, task_id: UUID, user_id: UUID) -> Optional[dict]:
        """
        Get a specific task by ID for the given user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = self.db_session.exec(statement).first()

        if not task:
            raise TaskNotFoundException(task_id)

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

    def get_tasks_by_user(self, user_id: UUID) -> List[dict]:
        """
        Get all tasks for the given user.
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = self.db_session.exec(statement).all()

        return [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": str(task.user_id),
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

    def update_task(self, task_id: UUID, user_id: UUID = None, **kwargs) -> Optional[dict]:
        """
        Update a specific task for the given user.
        """
        statement = select(Task).where(Task.id == task_id)
        if user_id:
            statement = statement.where(Task.user_id == user_id)
        db_task = self.db_session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        # Update only the fields that are provided
        for field, value in kwargs.items():
            if hasattr(db_task, field):
                setattr(db_task, field, value)

        db_task.updated_at = __import__('datetime').datetime.utcnow()
        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at.isoformat(),
            "updated_at": db_task.updated_at.isoformat()
        }

    def delete_task(self, task_id: UUID) -> bool:
        """
        Delete a specific task.
        """
        statement = select(Task).where(Task.id == task_id)
        db_task = self.db_session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        self.db_session.delete(db_task)
        self.db_session.commit()

        return True

    def toggle_task_completion(self, task_id: UUID, user_id: UUID) -> Optional[dict]:
        """
        Toggle the completion status of a specific task for the given user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = self.db_session.exec(statement).first()

        if not db_task:
            raise TaskNotFoundException(task_id)

        # Toggle the completion status
        db_task.completed = not db_task.completed
        db_task.updated_at = __import__('datetime').datetime.utcnow()

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        return {
            "id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": str(db_task.user_id),
            "created_at": db_task.created_at.isoformat(),
            "updated_at": db_task.updated_at.isoformat()
        }