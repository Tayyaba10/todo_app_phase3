import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from uuid import uuid4
from backend.src.main import app
from backend.src.services.agent_service import AgentService


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_chat_endpoint_success(client):
    """Test the chat endpoint with a valid request."""
    user_id = str(uuid4())

    # Mock the AgentService
    mock_agent_service = Mock(spec=AgentService)
    mock_agent_service.process_user_message = Mock(return_value={
        "response": "I've added the task 'buy groceries' to your list.",
        "conversation_id": str(uuid4()),
        "tool_calls": []
    })

    # Mock the database session
    mock_db_session = Mock()

    with patch('backend.src.api.routes.chat.AgentService', return_value=mock_agent_service), \
         patch('backend.src.api.routes.chat.get_session', return_value=mock_db_session), \
         patch('backend.src.api.deps.verify_token', return_value={'user_id': user_id, 'email': 'test@example.com'}):

        # Set a fake JWT token (normally this would be a valid signed token)
        headers = {"Authorization": "Bearer fake-jwt-token"}

        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Add a task to buy groceries"},
            headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert data["response"] == "I've added the task 'buy groceries' to your list."


def test_chat_endpoint_missing_auth(client):
    """Test the chat endpoint without authentication."""
    user_id = str(uuid4())

    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": "Add a task to buy groceries"}
    )

    assert response.status_code == 403  # Should require authentication


def test_chat_endpoint_invalid_user_id(client):
    """Test the chat endpoint with mismatched user ID."""
    user_id1 = str(uuid4())
    user_id2 = str(uuid4())

    # Mock authentication to return a different user ID
    with patch('backend.src.api.deps.verify_token', return_value={'user_id': user_id1, 'email': 'test@example.com'}):
        headers = {"Authorization": "Bearer fake-jwt-token"}

        response = client.post(
            f"/api/{user_id2}/chat",
            json={"message": "Add a task to buy groceries"},
            headers=headers
        )

        assert response.status_code == 403  # Forbidden due to user ID mismatch


@pytest.mark.asyncio
async def test_chat_endpoint_with_conversation_id(client):
    """Test the chat endpoint with an existing conversation ID."""
    user_id = str(uuid4())
    conversation_id = str(uuid4())

    # Mock the AgentService
    mock_agent_service = Mock(spec=AgentService)
    mock_agent_service.process_user_message = Mock(return_value={
        "response": "I've added another task for you.",
        "conversation_id": conversation_id,
        "tool_calls": []
    })

    # Mock the database session
    mock_db_session = Mock()

    with patch('backend.src.api.routes.chat.AgentService', return_value=mock_agent_service), \
         patch('backend.src.api.routes.chat.get_session', return_value=mock_db_session), \
         patch('backend.src.api.deps.verify_token', return_value={'user_id': user_id, 'email': 'test@example.com'}):

        headers = {"Authorization": "Bearer fake-jwt-token"}

        response = client.post(
            f"/api/{user_id}/chat",
            json={
                "message": "Add another task",
                "conversation_id": conversation_id
            },
            headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == conversation_id


def test_health_check_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/api/chat/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "chat-api"