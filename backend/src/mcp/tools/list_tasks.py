"""
List Tasks MCP Tool

Implements the list_tasks MCP tool that allows AI agents to retrieve
a user's todo items with optional filtering. The tool validates user
authentication and enforces data isolation.
"""

from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session
from ...services.task_service import TaskService


class ListTasksTool:
    """
    MCP tool for listing tasks.

    This tool enables AI agents to retrieve a user's todo items with optional
    filtering capabilities while maintaining proper authentication validation
    and user data isolation.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = TaskService(db_session)

    def execute(self, user_id: UUID, completed: bool = None) -> Dict[str, Any]:
        """
        Execute the list_tasks operation.

        Args:
            user_id: The ID of the authenticated user
            completed: Optional filter for completion status
                     None = all tasks, True = completed only, False = pending only

        Returns:
            Dictionary with the result of the operation
        """
        try:
            # Get tasks for user using service layer (includes ownership validation)
            all_tasks = self.task_service.get_tasks_by_user(user_id)

            # Filter by completion status if specified
            if completed is not None:
                filtered_tasks = [task for task in all_tasks if task["completed"] == completed]
            else:
                filtered_tasks = all_tasks

            return {
                "status": "success",
                "message": f"Retrieved {len(filtered_tasks)} tasks",
                "tasks": filtered_tasks
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to list tasks: {str(e)}"
            }


# Example usage function for testing
def create_list_tasks_tool(db_session: Session):
    """
    Factory function to create a ListTasksTool instance.

    Args:
        db_session: Database session for the operation

    Returns:
        Configured ListTasksTool instance
    """
    return ListTasksTool(db_session)