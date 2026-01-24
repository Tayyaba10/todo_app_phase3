# Feature Specification: Todo App Phase-II Backend API & Database

**Feature Branch**: `1-todo-api-backend`
**Created**: 2026-01-08
**Status**: Draft
**Input**: User description: "Todo App Phase-II Backend API & Database

Target audience:
- Hackathon evaluators reviewing backend correctness
- Developers consuming the API from a Next.js frontend
- Security reviewers validating JWT-based access control

Focus:
- RESTful API design for task management
- Secure, JWT-authenticated access
- Persistent storage using Neon PostgreSQL
- Strict user-level data isolation

Success criteria:
- All CRUD task operations implemented via REST endpoints
- Every endpoint requires a valid JWT token
- Authenticated user identity is derived exclusively from JWT
- Users can only access and modify their own tasks
- Backend successfully integrates with Better Auth JWTs
- API responses use correct HTTP status codes
- Database persistence verified via Neon PostgreSQL

Constraints:
- Backend framework: FastAPI (Python)
- ORM: SQLModel only
- Database: Neon Serverless PostgreSQL
- Authentication: JWT verification using BETTER_AUTH_SECRET
- No session-based or cookie-based authentication
- No manual coding; implementation via Claude Code only
- API must be compatible with Next.js App Router frontend

Required API endpoints:
- GET    /api/tasks                → List authenticated user's tasks
- POST   /api/tasks                → Create new task
- GET    /api/tasks/{id}            → Retrieve task details
- PUT    /api/tasks/{id}            → Update task
- DELETE /api/tasks/{id}            → Delete task
- PATCH  /api/tasks/{id}/complete   → Toggle completion

Security requirements:
- JWT extracted from Authorization: Bearer <token> header
- Token signature verified using shared secret
- Expired or invalid tokens return HTTP 401
- Cross-user access attempts return HTTP 403
- User ID in URL must match JWT subject (or be removed entirely)

Data requirements:
- Each task must be associated with exactly one user
- Task ownership enforced at query level
- Database schema must"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a new task (Priority: P1)

As an authenticated user, I want to create a new task so that I can track my to-dos. The system should securely store my task in the database and associate it with my user account using JWT-based authentication.

**Why this priority**: This is the foundational functionality that allows users to add tasks to the system, which is essential for the core value proposition of the todo app.

**Independent Test**: Can be fully tested by making a POST request to /api/tasks with a valid JWT token and task data, and verifying that the task is created and stored in the database with the correct user association.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user makes a POST request to /api/tasks with valid task data, **Then** the task is created and associated with the user's account
2. **Given** user has an invalid or expired JWT token, **When** user makes a POST request to /api/tasks, **Then** the system returns HTTP 401 Unauthorized

---

### User Story 2 - View user's own tasks (Priority: P1)

As an authenticated user, I want to view all my tasks so that I can see what I need to do. The system should only show tasks that belong to the authenticated user based on their JWT token.

**Why this priority**: This is the core functionality for task visibility, ensuring users can see their tasks while maintaining proper data isolation between users.

**Independent Test**: Can be fully tested by making a GET request to /api/tasks with a valid JWT token and verifying that only tasks belonging to that user are returned.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user makes a GET request to /api/tasks, **Then** the system returns only tasks associated with that user's account
2. **Given** user has an invalid or expired JWT token, **When** user makes a GET request to /api/tasks, **Then** the system returns HTTP 401 Unauthorized

---

### User Story 3 - Update and manage individual tasks (Priority: P2)

As an authenticated user, I want to update, delete, and mark tasks as complete so that I can manage my to-do list effectively. The system should ensure I can only modify tasks that belong to me.

**Why this priority**: This provides the essential CRUD operations for task management, allowing users to maintain their task lists over time.

**Independent Test**: Can be fully tested by making GET, PUT, DELETE, and PATCH requests to /api/tasks/{id} with a valid JWT token and verifying that operations only succeed for tasks belonging to the authenticated user.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token and owns a specific task, **When** user makes a PUT request to /api/tasks/{id} with updated task data, **Then** the task is updated successfully
2. **Given** user is authenticated with a valid JWT token and owns a specific task, **When** user makes a PATCH request to /api/tasks/{id}/complete, **Then** the task's completion status is toggled
3. **Given** user is authenticated with a valid JWT token but does not own a specific task, **When** user makes a PUT request to /api/tasks/{id}, **Then** the system returns HTTP 403 Forbidden

---

### Edge Cases

- What happens when a user tries to access a task that doesn't exist?
- How does the system handle expired JWT tokens during API requests?
- What happens when a user tries to access another user's tasks?
- How does the system handle malformed JWT tokens?
- What occurs when the database is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide RESTful API endpoints for task management operations
- **FR-002**: System MUST require a valid JWT token for all API endpoints
- **FR-003**: System MUST verify JWT token signature using BETTER_AUTH_SECRET
- **FR-004**: System MUST extract authenticated user identity exclusively from JWT token
- **FR-005**: System MUST ensure users can only access and modify their own tasks
- **FR-006**: System MUST store task data persistently in Neon PostgreSQL database
- **FR-007**: System MUST return appropriate HTTP status codes (200, 201, 401, 403, 404, etc.)
- **FR-008**: System MUST implement the following API endpoints: GET /api/tasks, POST /api/tasks, GET /api/tasks/{id}, PUT /api/tasks/{id}, DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete
- **FR-009**: System MUST associate each task with exactly one user
- **FR-010**: System MUST enforce task ownership at the query level to prevent cross-user access
- **FR-011**: System MUST return HTTP 401 for expired or invalid tokens
- **FR-012**: System MUST return HTTP 403 for cross-user access attempts

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's to-do item with attributes like title, description, completion status, and creation timestamp
- **User**: Represents an authenticated user identified by their JWT subject, associated with multiple tasks
- **JWT Token**: Security token containing user identity information, verified using shared secret

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All CRUD task operations are successfully implemented via REST endpoints
- **SC-002**: Every API endpoint requires and validates a JWT token for access
- **SC-003**: Authenticated user identity is correctly derived from JWT token exclusively
- **SC-004**: Users can only access and modify their own tasks, with cross-user access properly prevented
- **SC-005**: Backend successfully integrates with Better Auth JWTs for authentication
- **SC-006**: API responses use correct HTTP status codes as specified in requirements
- **SC-007**: Database persistence is verified and working with Neon PostgreSQL
- **SC-008**: System passes hackathon evaluation checklist for backend correctness
- **SC-009**: API is compatible with Next.js App Router frontend integration