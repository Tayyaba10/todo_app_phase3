---
id: 0001
title: "phase-iii-constitution-update"
stage: constitution
date_iso: 2026-01-23
surface: agent
model: claude-sonnet-4-5-20250929
feature: "none"
branch: "main"
user: "developer"
command: "/sp.phr"
labels: ["constitution", "ai-native", "mcp", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml:
  - "none"
---

# PHR-0001: Phase-III Constitution Update

## PROMPT_TEXT

```
/sp.constitution

Project: Phase-III Todo AI Chatbot (AI-Native Task Management System)

Core principles:
- AI-native design (agents act via tools, not hardcoded logic)
- Stateless server architecture with persistent state in database
- Deterministic tool execution (AI decides, tools execute)
- Clear separation of reasoning, action, and presentation layers
- Spec-driven, reviewable development (no manual coding)

Key standards:
- All AI actions must occur through explicitly defined MCP tools
- MCP tools must be stateless and persist all state to database
- Conversation context must be reconstructed from database on every request
- AI agent must never directly modify database without MCP tools
- User identity must be enforced consistently across chat, tools, and storage

Architectural rules:
- Chat endpoint holds no in-memory session state
- Conversation history is the single source of truth for context
- Agent reasoning layer is isolated from task execution layer
- MCP server exposes only task-related operations as tools
- Frontend communicates only via chat API (no direct task mutation)

Technology constraints:
- Frontend: OpenAI ChatKit
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK only
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Shared identity derived from authenticated user only

Security & identity rules:
- All chat requests require valid JWT authentication
- User identity must be derived from JWT, never from free-form input
- MCP tools must validate user ownership on every operation
- Cross-user task or conversation access is strictly forbidden
- Unauthorized access returns HTTP 401
- Forbidden access returns HTTP 403

Data integrity standards:
- Every user message is persisted before agent execution
- Every assistant response is persisted after agent execution
- Tool calls and outcomes must be traceable
- Database schema must support conversation replay after server restart
- No hidden or implicit state allowed in server memory

AI behavior standards:
- Agent must select tools based on user intent
- Agent must confirm actions in natural language
- Agent must handle ambiguity gracefully
- Agent must recover from tool errors with user-friendly responses
- Agent must not hallucinate task state outside database results

Constraints:
- No manual code writing (Claude Code only)
- No direct REST task manipulation from chat UI
- No background workers or long-lived processes
- No real-time streaming required (single request-response cycle)
- No external vector databases or memory stores

Success criteria:
- Users can manage todos via natural language
- AI uses MCP tools correctly and consistently
- Conversation context persists across requests and restarts
- System remains fully stateless at server level
- Architecture is reviewable, explainable, and reproducible
- Phase-III functionality passes hackathon evaluation checklist
```

## RESPONSE_TEXT

Updated the project constitution to reflect Phase-III requirements focusing on AI-native design, MCP tools, and stateless architecture. The new constitution emphasizes AI-native design principles, stateless server architecture, MCP tool enforcement, data integrity, and identity security.

## OUTCOME_IMPACT

Successfully updated the constitution file at .specify/memory/constitution.md to version 2.0.0, reflecting the transition from Phase-II to Phase-III with focus on AI-native design and MCP architecture. The constitution now properly guides development toward an AI-driven task management system with stateless server architecture.

## TESTS_SUMMARY

none

## FILES_SUMMARY

- .specify/memory/constitution.md

## NEXT_PROMPTS

none

## REFLECTION_NOTE

The constitution update successfully captures the shift from traditional web application to AI-native architecture with emphasis on MCP tools and stateless design.

## EVALUATION

Failure modes observed: The create-phr.sh script did not produce expected output, requiring manual creation of the PHR file.

Next experiment to improve prompt quality: Verify the PHR creation script functionality and ensure proper error handling in the future.