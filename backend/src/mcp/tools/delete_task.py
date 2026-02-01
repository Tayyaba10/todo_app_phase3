"""
Delete Task MCP Tool

Implements the delete_task MCP tool that allows AI agents to remove todo items
from the system. The tool validates user authentication, enforces ownership,
and removes the task from the database.
"""

from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session
from ...services.task_service import TaskService


class DeleteTaskTool:
    """
    MCP tool for deleting tasks.

    This tool enables AI agents to remove todo items by providing
    a standardized interface that validates user authentication,
    enforces ownership, and ensures proper data removal.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = TaskService(db_session)

    def execute(self, user_id: UUID, task_id: UUID) -> Dict[str, Any]:
        """
        Execute the delete_task operation.

        Args:
            user_id: The ID of the authenticated user
            task_id: The ID of the task to delete

        Returns:
            Dictionary with the result of the operation
        """
        try:
            # Delete task using service layer (includes ownership validation)
            success = self.task_service.delete_task(task_id, user_id)

            if success:
                return {
                    "status": "success",
                    "message": "Task deleted successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": "Task not found or unauthorized access"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete task: {str(e)}"
            }


# Example usage function for testing
def create_delete_task_tool(db_session: Session):
    """
    Factory function to create a DeleteTaskTool instance.

    Args:
        db_session: Database session for the operation

    Returns:
        Configured DeleteTaskTool instance
    """
    return DeleteTaskTool(db_session)