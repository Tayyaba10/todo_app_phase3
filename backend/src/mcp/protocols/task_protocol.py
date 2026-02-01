"""
Task Protocol Definitions for MCP Server

Defines the standardized contracts for task management tools exposed via MCP.
These protocols ensure consistent interfaces for AI agents to interact with
todo functionality while maintaining security and user ownership validation.
"""

from typing import Protocol, Dict, Any, List, Optional
from uuid import UUID


class TaskProtocol(Protocol):
    """
    Protocol defining the interface for task management tools.

    This protocol ensures that all task management tools follow a consistent
    interface for use with the MCP server while maintaining statelessness
    and user ownership validation.
    """

    def add_task(self, user_id: UUID, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a new task for the specified user.

        Args:
            user_id: The ID of the user requesting the operation
            title: The title of the task to create
            description: Optional description of the task

        Returns:
            Dictionary with task creation result containing:
            - status: "success" or "error"
            - message: Human-readable result message
            - task_id: ID of created task (on success)
            - task_details: Full task information (on success)
        """
        ...

    def list_tasks(self, user_id: UUID, completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        List tasks for the specified user.

        Args:
            user_id: The ID of the user requesting the operation
            completed: Optional filter for completion status
                     None = all tasks, True = completed only, False = pending only

        Returns:
            Dictionary with task listing result containing:
            - status: "success" or "error"
            - message: Human-readable result message
            - tasks: List of task dictionaries
        """
        ...

    def update_task(self, user_id: UUID, task_id: UUID, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        Update an existing task for the specified user.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            Dictionary with task update result containing:
            - status: "success" or "error"
            - message: Human-readable result message
            - task_details: Updated task information (on success)
        """
        ...

    def complete_task(self, user_id: UUID, task_id: UUID) -> Dict[str, Any]:
        """
        Mark a task as complete for the specified user.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to mark as complete

        Returns:
            Dictionary with task completion result containing:
            - status: "success" or "error"
            - message: Human-readable result message
            - task_details: Updated task information (on success)
        """
        ...

    def delete_task(self, user_id: UUID, task_id: UUID) -> Dict[str, Any]:
        """
        Delete a task for the specified user.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to delete

        Returns:
            Dictionary with task deletion result containing:
            - status: "success" or "error"
            - message: Human-readable result message
        """
        ...

    def process_tool_call(self, tool_name: str, tool_args: Dict[str, Any], auth_token: str) -> Dict[str, Any]:
        """
        Process a tool call from an AI agent.

        Validates authentication, enforces user ownership, and executes the requested tool.

        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments for the tool
            auth_token: JWT authentication token from the agent

        Returns:
            Result of tool execution
        """
        ...