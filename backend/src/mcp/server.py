"""
MCP Server for Todo Task Management Tools

Implements an MCP (Model Context Protocol) server that exposes todo operations
as standardized tools for AI agents to use. The server provides stateless,
authenticated access to task management functionality with user ownership validation.
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
import json
from sqlmodel import Session
from ..services.task_service import TaskService
from ..services.conversation_service import ConversationService
from ..core.auth import verify_token


class MCPTaskServer:
    """
    MCP Server implementation for task management tools.

    Provides standardized tools for AI agents to perform todo operations
    while maintaining statelessness and enforcing user ownership validation.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = TaskService(db_session)
        self.conversation_service = ConversationService(db_session)

    def add_task(self, user_id: UUID, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP tool for adding a new task.

        Args:
            user_id: The ID of the user requesting the operation
            title: The title of the task to create
            description: Optional description of the task

        Returns:
            Dictionary with task creation result
        """
        try:
            # Create task using service layer
            result = self.task_service.create_task(
                user_id=user_id,
                title=title,
                description=description or "",
                completed=False
            )

            return {
                "status": "success",
                "message": f"Task '{title}' created successfully",
                "task_id": result["id"],
                "task_details": result
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create task: {str(e)}"
            }

    def list_tasks(self, user_id: UUID, completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        MCP tool for listing tasks.

        Args:
            user_id: The ID of the user requesting the operation
            completed: Optional filter for completion status (None for all, True for completed, False for pending)

        Returns:
            Dictionary with list of tasks
        """
        try:
            # Get tasks for user using service layer
            tasks = self.task_service.get_tasks_by_user(user_id)

            # Filter by completion status if specified
            if completed is not None:
                tasks = [task for task in tasks if task["completed"] == completed]

            return {
                "status": "success",
                "message": f"Retrieved {len(tasks)} tasks",
                "tasks": tasks
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to list tasks: {str(e)}"
            }

    def update_task(self, user_id: UUID, task_id: UUID, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        MCP tool for updating a task.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            Dictionary with update result
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

            # Update task using service layer
            result = self.task_service.update_task(
                task_id=task_id,
                user_id=user_id,
                **update_data
            )

            return {
                "status": "success",
                "message": f"Task updated successfully",
                "task_details": result
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update task: {str(e)}"
            }

    def complete_task(self, user_id: UUID, task_id: UUID) -> Dict[str, Any]:
        """
        MCP tool for marking a task as complete.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to mark as complete

        Returns:
            Dictionary with completion result
        """
        try:
            # Toggle task completion using service layer
            result = self.task_service.toggle_task_completion(task_id, user_id)

            status_msg = "completed" if result["completed"] else "marked as incomplete"
            return {
                "status": "success",
                "message": f"Task {status_msg} successfully",
                "task_details": result
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to complete task: {str(e)}"
            }

    def delete_task(self, user_id: UUID, task_id: UUID) -> Dict[str, Any]:
        """
        MCP tool for deleting a task.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to delete

        Returns:
            Dictionary with deletion result
        """
        try:
            # Delete task using service layer
            success = self.task_service.delete_task(task_id, user_id)

            if success:
                return {
                    "status": "success",
                    "message": "Task deleted successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": "Task not found or unauthorized"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete task: {str(e)}"
            }

    def process_tool_call(self, tool_name: str, tool_args: Dict[str, Any], auth_token: str) -> Dict[str, Any]:
        """
        Process an incoming tool call from an AI agent.

        Validates authentication, enforces user ownership, and executes the requested tool.

        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments for the tool
            auth_token: JWT authentication token from the agent

        Returns:
            Result of tool execution
        """
        # Verify authentication token
        user_payload = verify_token(auth_token)
        if not user_payload:
            return {
                "status": "error",
                "message": "Invalid or expired authentication token"
            }

        user_id = UUID(user_payload.get("user_id"))

        # Validate user ownership where applicable
        if "task_id" in tool_args:
            task_id = UUID(tool_args["task_id"])
            # We'll validate ownership in the service layer, but we can also do a quick check here
            try:
                task = self.task_service.get_task_by_id(task_id, user_id)
                if not task:
                    return {
                        "status": "error",
                        "message": "Unauthorized: You don't have access to this task"
                    }
            except:
                return {
                    "status": "error",
                    "message": "Unauthorized: You don't have access to this task"
                }

        # Execute the appropriate tool based on name
        if tool_name == "add_task":
            return self.add_task(
                user_id=user_id,
                title=tool_args.get("title", ""),
                description=tool_args.get("description")
            )
        elif tool_name == "list_tasks":
            completed_filter = tool_args.get("completed")
            return self.list_tasks(user_id=user_id, completed=completed_filter)
        elif tool_name == "update_task":
            return self.update_task(
                user_id=user_id,
                task_id=UUID(tool_args["task_id"]),
                title=tool_args.get("title"),
                description=tool_args.get("description"),
                completed=tool_args.get("completed")
            )
        elif tool_name == "complete_task":
            return self.complete_task(
                user_id=user_id,
                task_id=UUID(tool_args["task_id"])
            )
        elif tool_name == "delete_task":
            return self.delete_task(
                user_id=user_id,
                task_id=UUID(tool_args["task_id"])
            )
        else:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool_name}"
            }