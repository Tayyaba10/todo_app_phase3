---
ID: 1
TITLE: Update CLAUDE.md with agent usage guidelines
STAGE: general
DATE_ISO: 2026-01-08
SURFACE: agent
MODEL: claude-sonnet-4-5-20250929
FEATURE: none
BRANCH: master
USER: user
COMMAND: Update the 'claude.md' file based on my project requirements.
LABELS: ["documentation", "agent-config"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - D:\hackathon2_todo_app\phase2\CLAUDE.md
TESTS_YAML: []
---
## Prompt
```
Update the 'claude.md' file based on my project requirements.
Inthis file:
-Use Auth Agent for authentication
-Use API Agent for API-related logic
-Use frontend Agent for frontend develkopment (e.g., Next.js)
-Use backend Agent for FastAPI development
-Use DB Agent for database design and operations

Below are my project requirements:
'''"""
Phase II: Todo Full-Stack Web Application
Basic Level Functionality
Objective: Using Claude Code and Spec-Kit Plus transform the console app into a modern multi-user web application with persistent storage.
💡Development Approach: Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. No manual coding allowed. We will review the process, prompts, and iterations to judge each phase and project.
Requirements
Implement all 5 Basic Level features as a web application
Create RESTful API endpoints
Build responsive frontend interface
Store data in Neon Serverless PostgreSQL database
Authentication – Implement user signup/signin using Better Auth
Technology Stack
Layer
Technology
Frontend
Next.js 16+ (App Router)
Backend
Python FastAPI
ORM
SQLModel
Database
Neon Serverless PostgreSQL
Spec-Driven
Claude Code + Spec-Kit Plus
Authentication
Better Auth

Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.
How It Works
User logs in on Frontend → Better Auth creates a session and issues a JWT token
Frontend makes API call → Includes the JWT token in the Authorization: Bearer <token> header
Backend receives request → Extracts token from header, verifies signature using shared secret
Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
Backend filters data → Returns only tasks belonging to that user
What Needs to Change

'''"""
```

## Response
Updated `CLAUDE.md` to include agent usage guidelines for authentication, frontend development (Next.js App Router), backend development (FastAPI), and database design and operations (Neon Serverless PostgreSQL).

## Outcome
The `CLAUDE.md` file was successfully updated to include the specified agent usage guidelines, aligning the project instructions with the chosen technology stack and agent capabilities.
