# Authentication Integration Guide

## Overview
This document describes the authentication system implemented for the Todo App, which uses JWT-based authentication with Better Auth on the frontend and FastAPI JWT verification on the backend.

## Architecture
- Frontend: Next.js 16+ with Better Auth client
- Backend: FastAPI with JWT token verification
- Authentication: JWT-only with shared secret via BETTER_AUTH_SECRET
- Storage: JWT tokens stored in browser localStorage

## Endpoints

### Authentication Endpoints
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate user and return JWT
- `GET /api/auth/profile` - Get authenticated user profile

### Protected Task Endpoints
All task endpoints require a valid JWT token in the Authorization header:
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

## JWT Token Structure
The JWT token contains the following claims:
- `sub`: User ID (subject)
- `email`: User's email address
- `name`: User's display name
- `exp`: Expiration timestamp

## Frontend Integration

### Authentication Context
The `AuthProvider` manages authentication state and provides the `useAuth` hook for components to access authentication data.

### API Service
The `apiService` automatically includes the JWT token in the Authorization header for all requests.

## Backend Integration

### JWT Verification
The `get_current_user` dependency verifies JWT tokens and extracts user identity from the token payload.

### User Isolation
All task operations are filtered by the authenticated user's ID to ensure data isolation.

## Security Considerations
- JWT tokens are validated using a shared secret (BETTER_AUTH_SECRET)
- All protected endpoints require a valid, non-expired JWT token
- User-specific data access is enforced through user ID filtering
- Passwords should be properly hashed in production (using bcrypt)

## Error Handling
- Invalid or expired tokens return HTTP 401 Unauthorized
- Insufficient permissions return HTTP 403 Forbidden
- Failed authentication returns HTTP 401 Unauthorized