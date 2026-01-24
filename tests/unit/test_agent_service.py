import pytest
from unittest.mock import Mock, patch, MagicMock
from uuid import uuid4
from backend.src.services.agent_service import AgentService
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message, SenderType


class TestAgentService:
    """Unit tests for AgentService"""

    def test_process_user_message_creates_new_conversation(self):
        """Test that process_user_message creates a new conversation when no conversation_id provided."""
        # Arrange
        db_session = Mock()
        agent_service = AgentService(db_session, "fake-openai-key")

        user_id = uuid4()
        message_content = "Add a task to buy groceries"

        # Mock the conversation service
        mock_conversation = Mock(spec=Conversation)
        mock_conversation.id = uuid4()
        agent_service.conversation_service.create_conversation = Mock(return_value=mock_conversation)

        # Mock the OpenAI client response
        mock_openai_response = Mock()
        mock_openai_response.choices = [Mock()]
        mock_openai_response.choices[0].message = Mock(content="I've added the task for you.")
        mock_openai_response.choices[0].tool_calls = None

        agent_service.openai_client.chat.completions.create = Mock(return_value=mock_openai_response)

        # Act
        result = agent_service.process_user_message(user_id, message_content)

        # Assert
        assert "response" in result
        assert "conversation_id" in result
        assert result["conversation_id"] == mock_conversation.id
        agent_service.conversation_service.create_conversation.assert_called_once()

    def test_process_user_message_uses_existing_conversation(self):
        """Test that process_user_message uses an existing conversation when conversation_id is provided."""
        # Arrange
        db_session = Mock()
        agent_service = AgentService(db_session, "fake-openai-key")

        user_id = uuid4()
        conversation_id = uuid4()
        message_content = "Add a task to buy groceries"

        # Mock the conversation service
        mock_conversation = Mock(spec=Conversation)
        mock_conversation.id = conversation_id
        agent_service.conversation_service.get_conversation_by_id_with_messages = Mock(return_value=mock_conversation)

        # Mock the OpenAI client response
        mock_openai_response = Mock()
        mock_openai_response.choices = [Mock()]
        mock_openai_response.choices[0].message = Mock(content="I've added the task for you.")
        mock_openai_response.choices[0].tool_calls = None

        agent_service.openai_client.chat.completions.create = Mock(return_value=mock_openai_response)

        # Act
        result = agent_service.process_user_message(user_id, message_content, conversation_id)

        # Assert
        assert result["conversation_id"] == conversation_id
        agent_service.conversation_service.get_conversation_by_id_with_messages.assert_called_once_with(conversation_id)

    def test_execute_tool_create_todo(self):
        """Test executing the create_todo tool."""
        # Arrange
        db_session = Mock()
        agent_service = AgentService(db_session, "fake-openai-key")

        # Mock the task service
        expected_result = {"id": str(uuid4()), "title": "Buy groceries", "completed": False}
        agent_service.task_service.create_task = Mock(return_value=expected_result)

        # Act
        result = agent_service._execute_tool("create_todo", {"title": "Buy groceries"}, uuid4())

        # Assert
        assert result == expected_result
        agent_service.task_service.create_task.assert_called_once()

    def test_execute_tool_list_todos(self):
        """Test executing the list_todos tool."""
        # Arrange
        db_session = Mock()
        agent_service = AgentService(db_session, "fake-openai-key")

        user_id = uuid4()
        expected_result = [{"id": str(uuid4()), "title": "Buy groceries", "completed": False}]
        agent_service.task_service.get_tasks_by_user = Mock(return_value=expected_result)

        # Act
        result = agent_service._execute_tool("list_todos", {}, user_id)

        # Assert
        assert result == expected_result
        agent_service.task_service.get_tasks_by_user.assert_called_once_with(user_id)

    def test_execute_tool_unknown_function(self):
        """Test executing an unknown function."""
        # Arrange
        db_session = Mock()
        agent_service = AgentService(db_session, "fake-openai-key")

        # Act
        result = agent_service._execute_tool("unknown_function", {}, uuid4())

        # Assert
        assert "error" in result
        assert "Unknown function: unknown_function" in result["error"]

    def test_execute_tool_with_retry_success_on_first_attempt(self):
        """Test that _execute_tool_with_retry succeeds on the first attempt."""
        # Arrange
        db_session = Mock()
        agent_service = AgentService(db_session, "fake-openai-key")

        # Mock the _execute_tool method to succeed
        expected_result = {"success": True}
        agent_service._execute_tool = Mock(return_value=expected_result)

        # Act
        result = agent_service._execute_tool_with_retry("create_todo", {"title": "Test"}, uuid4())

        # Assert
        assert result == expected_result
        agent_service._execute_tool.assert_called_once()

    def test_handle_tool_execution_errors(self):
        """Test handling different types of tool execution errors."""
        # Arrange
        db_session = Mock()
        agent_service = AgentService(db_session, "fake-openai-key")

        # Test with error dictionary
        error_result = {"error": "Something went wrong"}
        error_output = agent_service._handle_tool_execution_errors(error_result)
        assert error_output == "Something went wrong"

        # Test with non-error result
        success_result = {"success": True}
        success_output = agent_service._handle_tool_execution_errors(success_result)
        assert success_output == str(success_result)

    def test_get_available_tools_contains_expected_functions(self):
        """Test that the available tools contain the expected functions."""
        # Arrange
        db_session = Mock()
        agent_service = AgentService(db_session, "fake-openai-key")

        # Act
        tools = agent_service._get_available_tools()

        # Assert
        assert len(tools) > 0
        tool_names = [tool["function"]["name"] for tool in tools]
        expected_tools = ["create_todo", "list_todos", "update_todo", "delete_todo", "request_clarification"]
        for expected_tool in expected_tools:
            assert expected_tool in tool_names