# Chat API Documentation

## Overview
The Chat API provides a conversational interface for managing todos using natural language. The API integrates with OpenAI Agents SDK to interpret user requests and execute appropriate MCP tools for todo management.

## Authentication
All endpoints require JWT authentication. Include the Authorization header with a valid JWT token:
```
Authorization: Bearer <your-jwt-token>
```

## Base URL
```
/api
```

## Endpoints

### POST /{user_id}/chat
Processes a natural language message through the AI agent and returns a response.

#### Parameters
- **user_id** (path): UUID - The ID of the authenticated user. Must match the user ID in the JWT token.

#### Request Body
```json
{
  "message": "string",
  "conversation_id": "string (optional, UUID)"
}
```

**Fields:**
- `message` (required): The natural language message from the user (e.g., "Create a task to buy groceries")
- `conversation_id` (optional): The ID of an existing conversation to continue. If omitted, a new conversation is created.

#### Response
```json
{
  "response": "string",
  "conversation_id": "string (UUID)",
  "tool_calls": "array"
}
```

**Fields:**
- `response`: The AI agent's response to the user's message
- `conversation_id`: The ID of the conversation (either the provided ID or the newly created one)
- `tool_calls`: Array of tools that were called during processing (for debugging purposes)

#### Example Request
```
POST /api/123e4567-e89b-12d3-a456-426614174000/chat
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "message": "Add a task to buy groceries",
  "conversation_id": "123e4567-e89b-12d3-a456-426614174001"
}
```

#### Example Response
```json
{
  "response": "I've added the task 'buy groceries' to your list.",
  "conversation_id": "123e4567-e89b-12d3-a456-426614174001",
  "tool_calls": [
    {
      "id": "call_abc123",
      "function": {
        "arguments": "{\"title\":\"buy groceries\"}",
        "name": "create_todo"
      },
      "type": "function"
    }
  ]
}
```

## Available Capabilities
The AI agent can understand and process various natural language commands related to todo management:

- **Creating todos**: "Add a task to...", "Create a todo for...", "I need to..."
- **Listing todos**: "Show my tasks", "What do I have to do?", "List my todos"
- **Completing todos**: "Mark X as complete", "Finish the Y task", "Complete Z"
- **Deleting todos**: "Delete the X task", "Remove Y from my list"
- **Updating todos**: "Change the title of X to Y", "Update the description of X"

## Rate Limits
The API implements rate limiting:
- 10 requests per minute per IP address

## Error Handling
The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (malformed request body)
- `401`: Unauthorized (invalid or missing JWT token)
- `403`: Forbidden (attempting to access another user's chat)
- `429`: Too many requests (rate limit exceeded)
- `500`: Internal server error

## Conversation Context
The system maintains conversation context by:
1. Loading the conversation history when a conversation_id is provided
2. Including the history in the agent's context for better understanding
3. Persisting both user and agent messages to maintain state
4. Allowing conversations to span multiple requests while maintaining context