---
id: 2
title: Create Todo App Backend API Spec
stage: spec
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-api-backend
branch: 1-todo-api-backend
user: user
command: sp.specify
labels: [spec, api, backend, todo]
links:
  spec: specs/1-todo-api-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-todo-api-backend/spec.md
 - specs/1-todo-api-backend/checklists/requirements.md
tests:
 - none
---

## Prompt

```
/sp.specify Todo App Phase-II Backend API & Database

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
- Database schema must
```

## Response snapshot

Created the specification file for the Todo App Phase-II Backend API & Database feature. The spec includes user scenarios for creating tasks, viewing tasks, and managing tasks with appropriate priority levels. Functional requirements cover JWT authentication, task CRUD operations, user isolation, and proper HTTP status codes. Success criteria are defined as measurable outcomes for the feature.

## Outcome

- ✅ Impact: Complete specification created for todo app backend API with security requirements
- 🧪 Tests: No tests required for specification creation
- 📁 Files: Created specs/1-todo-api-backend/spec.md and checklists/requirements.md
- 🔁 Next prompts: Ready to proceed with planning phase (/sp.plan)
- 🧠 Reflection: Specification covers all required API endpoints and security requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Proceed with feature planning