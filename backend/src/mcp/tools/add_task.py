"""
Add Task MCP Tool

Implements the add_task MCP tool that allows AI agents to create new todo items
through natural language processing. The tool validates user authentication,
enforces ownership, and persists the task to the database.
"""

from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session
from ...services.task_service import TaskService


class AddTaskTool:
    """
    MCP tool for adding new tasks.

    This tool enables AI agents to create new todo items by providing
    a standardized interface that validates user authentication and
    enforces proper data persistence.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = TaskService(db_session)

    def execute(self, user_id: UUID, title: str, description: str = None) -> Dict[str, Any]:
        """
        Execute the add_task operation.

        Args:
            user_id: The ID of the authenticated user
            title: The title of the task to create
            description: Optional description of the task

        Returns:
            Dictionary with the result of the operation
        """
        try:
            # Validate inputs
            if not title or not title.strip():
                return {
                    "status": "error",
                    "message": "Task title is required and cannot be empty"
                }

            # Create task using service layer (includes ownership validation)
            task_result = self.task_service.create_task(
                user_id=user_id,
                title=title.strip(),
                description=description.strip() if description else "",
                completed=False
            )

            return {
                "status": "success",
                "message": f"Task '{title}' created successfully",
                "task_id": task_result["id"],
                "task_details": {
                    "id": task_result["id"],
                    "title": task_result["title"],
                    "description": task_result["description"],
                    "completed": task_result["completed"],
                    "created_at": task_result["created_at"]
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create task: {str(e)}"
            }


# Example usage function for testing
def create_add_task_tool(db_session: Session):
    """
    Factory function to create an AddTaskTool instance.

    Args:
        db_session: Database session for the operation

    Returns:
        Configured AddTaskTool instance
    """
    return AddTaskTool(db_session)