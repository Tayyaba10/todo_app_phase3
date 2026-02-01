"""
Complete Task MCP Tool

Implements the complete_task MCP tool that allows AI agents to mark todo items
as completed or incomplete. The tool validates user authentication, enforces
ownership, and updates the task in the database.
"""

from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session
from ...services.task_service import TaskService


class CompleteTaskTool:
    """
    MCP tool for completing tasks.

    This tool enables AI agents to mark todo items as completed or toggle
    their completion status by providing a standardized interface that
    validates user authentication and enforces proper data persistence.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = TaskService(db_session)

    def execute(self, user_id: UUID, task_id: UUID) -> Dict[str, Any]:
        """
        Execute the complete_task operation.

        Args:
            user_id: The ID of the authenticated user
            task_id: The ID of the task to toggle completion status

        Returns:
            Dictionary with the result of the operation
        """
        try:
            # Toggle task completion using service layer (includes ownership validation)
            task_result = self.task_service.toggle_task_completion(task_id, user_id)

            status_msg = "completed" if task_result["completed"] else "marked as incomplete"
            return {
                "status": "success",
                "message": f"Task {status_msg} successfully",
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
                "message": f"Failed to complete task: {str(e)}"
            }


# Example usage function for testing
def create_complete_task_tool(db_session: Session):
    """
    Factory function to create a CompleteTaskTool instance.

    Args:
        db_session: Database session for the operation

    Returns:
        Configured CompleteTaskTool instance
    """
    return CompleteTaskTool(db_session)