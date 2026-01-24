---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: sp.constitution
labels: [constitution, governance, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: Phase-II Todo Full-Stack Web Application (Agentic Dev Stack)

Core principles:
- Spec-driven development (no manual coding)
- Security-first architecture (JWT-based authentication)
- Clear separation of concerns (Auth, Backend, Frontend)
- Deterministic and reproducible outputs
- Reviewability of prompts, plans, and iterations

Key standards:
- Every feature must trace back to a written spec requirement
- Authentication must be enforced on every protected route
- API behavior must be explicitly defined (inputs, outputs, errors)
- Frontend must consume backend strictly via documented APIs
- Environment variables must be clearly specified and consistent

Constraints:
- No manual code writing (Claude Code only)
- Stack is fixed and non-negotiable:
  - Frontend: Next.js 16+ (App Router)
  - Backend: FastAPI (Python)
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth (JWT)
- JWT secret must be shared via BETTER_AUTH_SECRET
- All API routes must require authentication after auth integration

Security rules:
- All API requests must verify JWT signature
- User ID must be derived from JWT, not client input
- Cross-user data access is strictly forbidden
- Unauthorized requests return HTTP 401
- Forbidden access returns HTTP 403

Success criteria:
- Multi-user task isolation works correctly
- Authenticated users only see their own tasks
- Frontend, backend, and auth integrate without manual glue code
- Specs → plans → tasks → implementation flow is reviewable
- Phase-II functionality passes hackathon evaluation checklist
```

## Response snapshot

Updated the constitution file with specific principles for the Phase-II Todo Full-Stack Web Application, replacing all template placeholders with concrete values based on the project requirements provided. The new constitution includes principles for spec-driven development, security-first architecture, clear separation of concerns, deterministic outputs, stack consistency, and authentication enforcement.

## Outcome

- ✅ Impact: Project constitution created with specific principles for the todo app project
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Ready to proceed with spec, plan, and task creation
- 🧠 Reflection: Constitution now provides clear governance framework for the project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Proceed with feature specification