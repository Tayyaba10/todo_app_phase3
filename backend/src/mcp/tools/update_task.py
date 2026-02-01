"""
Update Task MCP Tool

Implements the update_task MCP tool that allows AI agents to modify existing
todo items. The tool validates user authentication, enforces ownership,
and persists the updated task to the database.
"""

from typing import Dict, Any, Optional
from uuid import UUID
from sqlmodel import Session
from ...services.task_service import TaskService


class UpdateTaskTool:
    """
    MCP tool for updating tasks.

    This tool enables AI agents to modify existing todo items by providing
    a standardized interface that validates user authentication, enforces
    ownership, and ensures proper data persistence.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = TaskService(db_session)

    def execute(self, user_id: UUID, task_id: UUID, title: Optional[str] = None,
                description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        Execute the update_task operation.

        Args:
            user_id: The ID of the authenticated user
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            completed: New completion status for the task (optional)

        Returns:
            Dictionary with the result of the operation
        """
        try:
            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if completed is not None:
                update_data["completed"] = completed

            # Validate that at least one field is being updated
            if not update_data:
                return {
                    "status": "error",
                    "message": "At least one field (title, description, or completed) must be provided for update"
                }

            # Update task using service layer (includes ownership validation)
            task_result = self.task_service.update_task(
                task_id=task_id,
                user_id=user_id,
                **update_data
            )

            return {
                "status": "success",
                "message": "Task updated successfully",
                "task_details": {
                    "id": task_result["id"],
                    "title": task_result["title"],
                    "description": task_result["description"],
                    "completed": task_result["completed"],
                    "updated_at": task_result["updated_at"]
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update task: {str(e)}"
            }


# Example usage function for testing
def create_update_task_tool(db_session: Session):
    """
    Factory function to create an UpdateTaskTool instance.

    Args:
        db_session: Database session for the operation

    Returns:
        Configured UpdateTaskTool instance
    """
    return UpdateTaskTool(db_session)