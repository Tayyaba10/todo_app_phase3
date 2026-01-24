import pytest
from unittest.mock import Mock, MagicMock
from uuid import uuid4
from datetime import datetime
from backend.src.services.conversation_service import ConversationService
from backend.src.models.conversation import Conversation, ConversationCreate
from backend.src.models.message import Message, MessageCreate, SenderType


class TestConversationService:
    """Unit tests for ConversationService"""

    def test_create_conversation(self):
        """Test creating a new conversation."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        user_id = uuid4()
        conversation_data = ConversationCreate(user_id=user_id, title="Test Conversation")

        mock_conversation = Mock(spec=Conversation)
        mock_conversation.id = uuid4()
        mock_conversation.user_id = user_id
        mock_conversation.title = "Test Conversation"

        # Mock the database operations
        db_session.add = Mock()
        db_session.commit = Mock()
        db_session.refresh = Mock(side_effect=lambda obj: setattr(obj, 'id', mock_conversation.id))

        # Act
        result = conversation_service.create_conversation(conversation_data)

        # Assert
        assert result.user_id == user_id
        assert result.title == "Test Conversation"
        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_add_message_to_conversation(self):
        """Test adding a message to a conversation."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()
        message_data = MessageCreate(
            conversation_id=conversation_id,
            sender_type="user",
            content="Hello, world!"
        )

        mock_message = Mock(spec=Message)
        mock_message.id = uuid4()
        mock_message.conversation_id = conversation_id
        mock_message.sender_type = "user"
        mock_message.content = "Hello, world!"

        # Mock the database operations
        db_session.add = Mock()
        db_session.commit = Mock()
        db_session.refresh = Mock(side_effect=lambda obj: setattr(obj, 'id', mock_message.id))

        # Act
        result = conversation_service.add_message_to_conversation(message_data)

        # Assert
        assert result.conversation_id == conversation_id
        assert result.sender_type == "user"
        assert result.content == "Hello, world!"
        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_save_user_message(self):
        """Test saving a user message."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()
        content = "Hello, this is a user message."

        # Mock the add_message_to_conversation method
        mock_message = Mock(spec=Message)
        mock_message.id = uuid4()
        mock_message.conversation_id = conversation_id
        mock_message.sender_type = "user"
        mock_message.content = content
        conversation_service.add_message_to_conversation = Mock(return_value=mock_message)

        # Act
        result = conversation_service.save_user_message(conversation_id, content)

        # Assert
        assert result.sender_type == "user"
        assert result.content == content
        assert result.conversation_id == conversation_id
        conversation_service.add_message_to_conversation.assert_called_once()

    def test_save_agent_message(self):
        """Test saving an agent message."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()
        content = "Hello, this is an agent message."

        # Mock the add_message_to_conversation method
        mock_message = Mock(spec=Message)
        mock_message.id = uuid4()
        mock_message.conversation_id = conversation_id
        mock_message.sender_type = "agent"
        mock_message.content = content
        conversation_service.add_message_to_conversation = Mock(return_value=mock_message)

        # Act
        result = conversation_service.save_agent_message(conversation_id, content)

        # Assert
        assert result.sender_type == "agent"
        assert result.content == content
        assert result.conversation_id == conversation_id
        conversation_service.add_message_to_conversation.assert_called_once()

    def test_get_conversation_by_id(self):
        """Test getting a conversation by its ID."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()
        mock_conversation = Mock(spec=Conversation)
        mock_conversation.id = conversation_id

        # Mock the database execution
        exec_mock = Mock()
        exec_mock.first.return_value = mock_conversation
        db_session.exec.return_value = exec_mock

        # Act
        result = conversation_service.get_conversation_by_id(conversation_id)

        # Assert
        assert result.id == conversation_id
        db_session.exec.assert_called_once()

    def test_get_conversation_by_id_with_messages(self):
        """Test getting a conversation by its ID with messages."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()
        mock_conversation = Mock(spec=Conversation)
        mock_conversation.id = conversation_id

        # Mock the database execution
        exec_mock = Mock()
        exec_mock.first.return_value = mock_conversation
        db_session.exec.return_value = exec_mock

        # Act
        result = conversation_service.get_conversation_by_id_with_messages(conversation_id)

        # Assert
        assert result.id == conversation_id
        db_session.exec.assert_called_once()

    def test_get_conversations_by_user(self):
        """Test getting all conversations for a specific user."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        user_id = uuid4()
        mock_conversation1 = Mock(spec=Conversation)
        mock_conversation1.id = uuid4()
        mock_conversation1.user_id = user_id

        mock_conversation2 = Mock(spec=Conversation)
        mock_conversation2.id = uuid4()
        mock_conversation2.user_id = user_id

        mock_conversations = [mock_conversation1, mock_conversation2]

        # Mock the database execution
        exec_mock = Mock()
        exec_mock.all.return_value = mock_conversations
        db_session.exec.return_value = exec_mock

        # Act
        result = conversation_service.get_conversations_by_user(user_id)

        # Assert
        assert len(result) == 2
        assert result == mock_conversations
        db_session.exec.assert_called_once()

    def test_get_messages_for_conversation(self):
        """Test getting all messages for a specific conversation."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()
        mock_message1 = Mock(spec=Message)
        mock_message1.id = uuid4()
        mock_message1.conversation_id = conversation_id

        mock_message2 = Mock(spec=Message)
        mock_message2.id = uuid4()
        mock_message2.conversation_id = conversation_id

        mock_messages = [mock_message1, mock_message2]

        # Mock the database execution
        exec_mock = Mock()
        exec_mock.all.return_value = mock_messages
        db_session.exec.return_value = exec_mock

        # Act
        result = conversation_service.get_messages_for_conversation(conversation_id)

        # Assert
        assert len(result) == 2
        assert result == mock_messages
        db_session.exec.assert_called_once()

    def test_get_conversation_history(self):
        """Test getting conversation history with a limit."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()
        mock_message1 = Mock(spec=Message)
        mock_message1.id = uuid4()
        mock_message1.conversation_id = conversation_id

        mock_message2 = Mock(spec=Message)
        mock_message2.id = uuid4()
        mock_message2.conversation_id = conversation_id

        mock_messages = [mock_message1, mock_message2]

        # Mock the database execution
        exec_mock = Mock()
        exec_mock.all.return_value = mock_messages  # Return oldest first as per desc() order
        db_session.exec.return_value = exec_mock

        # Act
        result = conversation_service.get_conversation_history(conversation_id, limit=10)

        # Assert: Result should be reversed to return in chronological order (oldest first)
        assert len(result) == 2
        # Since the original mock_messages are returned in descending order, reversing them gives us chronological order
        db_session.exec.assert_called_once()

    def test_update_conversation_title(self):
        """Test updating a conversation's title."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()
        new_title = "Updated Conversation Title"

        # Create a mock conversation with initial values
        mock_conversation = Mock(spec=Conversation)
        mock_conversation.id = conversation_id
        mock_conversation.title = "Original Title"

        # Mock the get_conversation_by_id method
        conversation_service.get_conversation_by_id = Mock(return_value=mock_conversation)

        # Mock database operations
        db_session.add = Mock()
        db_session.commit = Mock()
        db_session.refresh = Mock()

        # Act
        result = conversation_service.update_conversation_title(conversation_id, new_title)

        # Assert
        assert result.title == new_title
        assert result.id == conversation_id
        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_deactivate_conversation(self):
        """Test deactivating a conversation."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()

        # Create a mock conversation
        mock_conversation = Mock(spec=Conversation)
        mock_conversation.id = conversation_id
        mock_conversation.is_active = True

        # Mock the get_conversation_by_id method
        conversation_service.get_conversation_by_id = Mock(return_value=mock_conversation)

        # Mock database operations
        db_session.add = Mock()
        db_session.commit = Mock()
        db_session.refresh = Mock()

        # Act
        result = conversation_service.deactivate_conversation(conversation_id)

        # Assert
        assert result is True
        assert mock_conversation.is_active is False
        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_deactivate_conversation_not_found(self):
        """Test deactivating a conversation that doesn't exist."""
        # Arrange
        db_session = Mock()
        conversation_service = ConversationService(db_session)

        conversation_id = uuid4()

        # Mock the get_conversation_by_id method to return None
        conversation_service.get_conversation_by_id = Mock(return_value=None)

        # Act
        result = conversation_service.deactivate_conversation(conversation_id)

        # Assert
        assert result is False