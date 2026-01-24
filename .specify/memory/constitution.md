<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 2.0.0
Added sections: AI-native design principles, MCP tool enforcement, Stateless architecture rules
Removed sections: Phase-II specific constraints
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Phase-III Todo AI Chatbot Constitution

## Core Principles

### AI-Native Design
All agent actions must occur through explicitly defined MCP tools; No hardcoded logic in AI agents; AI agents act via tools, not predetermined behavior; Reasoning, action, and presentation layers must be clearly separated.

### Stateless Server Architecture
Server maintains no in-memory session state; All state persisted to database; Conversation context reconstructed from database on every request; Deterministic tool execution where AI decides and tools execute.

### MCP Tool Enforcement
All AI actions must occur through explicitly defined MCP tools; MCP tools must be stateless and persist all state to database; MCP server exposes only task-related operations as tools; Frontend communicates only via chat API (no direct task mutation).

### Data Integrity and Persistence
Every user message is persisted before agent execution; Every assistant response is persisted after agent execution; Tool calls and outcomes must be traceable; Database schema must support conversation replay after server restart.

### Identity and Security Enforcement
All chat requests require valid JWT authentication; User identity must be derived from JWT, never from free-form input; MCP tools must validate user ownership on every operation; Cross-user task or conversation access is strictly forbidden.

### Conversation as Single Source of Truth
Conversation history is the single source of truth for context; Agent reasoning layer is isolated from task execution layer; Chat endpoint holds no in-memory session state; System remains fully stateless at server level.

## Additional Constraints

All AI behavior must follow established standards without hallucination; No manual code writing (Claude Code only); No direct REST task manipulation from chat UI; No background workers or long-lived processes; Every user message must trigger persistence before agent execution.

## Development Workflow

Spec-driven, reviewable development (no manual coding); AI agent must select tools based on user intent; Agent must confirm actions in natural language; Agent must handle ambiguity gracefully; Agent must recover from tool errors with user-friendly responses.

## Technology Stack

Frontend: OpenAI ChatKit; Backend: Python FastAPI; AI Framework: OpenAI Agents SDK; MCP Server: Official MCP SDK only; ORM: SQLModel; Database: Neon Serverless PostgreSQL; Authentication: Better Auth (JWT-based).

## Governance

This constitution supersedes all other practices; Amendments require documentation, approval, and migration plan; All PRs/reviews must verify compliance with AI-native, stateless, and MCP tool requirements; Code quality, testing, performance, security, and architecture principles must align with these requirements.

**Version**: 2.0.0 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-01-23