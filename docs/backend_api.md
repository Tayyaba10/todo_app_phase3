# Todo App Backend API Documentation

## Overview

This document describes the API endpoints for the Todo App Backend. All endpoints require JWT authentication in the Authorization header.

## Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

The JWT token should contain user information that will be used to enforce user-level data isolation.

## Base URL

All endpoints are prefixed with `/api`.

## Endpoints

### Create a New Task

**POST** `/api/tasks`

Creates a new task for the authenticated user.

#### Request Body

```json
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "completed": false
}
```

#### Response

**Status Code**: 201 Created

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Get All User's Tasks

**GET** `/api/tasks`

Retrieves all tasks belonging to the authenticated user.

#### Response

**Status Code**: 200 OK

```json
[
  {
    "id": 1,
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "user_id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

### Get a Specific Task

**GET** `/api/tasks/{task_id}`

Retrieves a specific task by ID for the authenticated user.

#### Parameters

- `task_id`: The ID of the task to retrieve

#### Response

**Status Code**: 200 OK

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Update a Task

**PUT** `/api/tasks/{task_id}`

Updates a specific task by ID for the authenticated user.

#### Parameters

- `task_id`: The ID of the task to update

#### Request Body

```json
{
  "title": "Updated task title (optional)",
  "description": "Updated task description (optional)",
  "completed": true
}
```

#### Response

**Status Code**: 200 OK

```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Delete a Task

**DELETE** `/api/tasks/{task_id}`

Deletes a specific task by ID for the authenticated user.

#### Parameters

- `task_id`: The ID of the task to delete

#### Response

**Status Code**: 200 OK

```json
{
  "message": "Task deleted successfully"
}
```

### Toggle Task Completion

**PATCH** `/api/tasks/{task_id}/complete`

Updates the completion status of a specific task by ID for the authenticated user.

#### Parameters

- `task_id`: The ID of the task to update

#### Request Body

```json
{
  "completed": true
}
```

#### Response

**Status Code**: 200 OK

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

## Error Handling

All endpoints return standard HTTP status codes:

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Unexpected server error

## Security

- All endpoints require JWT authentication
- Users can only access and modify their own tasks
- Input validation is performed on all requests