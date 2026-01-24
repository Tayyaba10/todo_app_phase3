# Research: Phase-III Todo AI Chat Agent

## Overview
This document captures research findings for implementing the stateless chat API with OpenAI Agents SDK integration for natural language todo management.

## Decision: OpenAI Agent Architecture
**Rationale**: The architecture needs to bridge the ChatKit frontend with MCP task tools through an intelligent agent that can interpret natural language and select appropriate tools.

**Alternatives considered**:
- Direct mapping of natural language to API calls: Would require complex regex/parsing logic and wouldn't handle varied user expressions well.
- Rule-based system: Would be inflexible and difficult to maintain as user expressions vary widely.
- OpenAI Functions vs Agents SDK: Functions provide more control but Agents SDK offers better orchestration and tool management.

## Decision: Conversation State Management
**Rationale**: Since the server must remain stateless but conversations need context, we'll load conversation history from the database before each agent invocation and persist new messages after.

**Alternatives considered**:
- In-memory caching: Violates statelessness requirement.
- Client-side storage: Would expose conversation data and not be reliable.
- Hybrid approach: Cache in memory briefly but always source of truth is DB.

## Decision: MCP Tool Registration
**Rationale**: The agent needs to access todo management functionality through MCP tools to maintain proper separation of concerns.

**Alternatives considered**:
- Direct database access from agent: Violates architecture constraint that agent only uses MCP tools.
- API endpoints as tools: Adds unnecessary complexity over direct MCP integration.
- Multiple specialized tools vs one generic tool: Multiple tools provide better specificity and error handling.

## Decision: JWT Authentication Strategy
**Rationale**: All chat requests must be authenticated to ensure user data isolation and security.

**Alternatives considered**:
- Session cookies: More complex for API consumption.
- API keys: Less suitable for user-specific data access.
- OAuth tokens: Overkill for this application scope.

## Decision: Message Persistence Strategy
**Rationale**: Both user messages and agent responses need to be persisted to maintain conversation history and context for future interactions.

**Alternatives considered**:
- Event sourcing: Overkill for this use case.
- Separate read/write models: Unnecessary complexity for current scale.
- Append-only log: Good for audit trail but need relational access for context loading.

## Technical Unknowns Resolved
- OpenAI Agents SDK integration patterns: Confirmed compatibility with FastAPI backend
- MCP tool registration process: Verified ability to register custom tools with agent
- Database query performance for conversation history: Planned indexing strategy for efficient loading
- JWT token validation in async context: Confirmed compatibility with FastAPI dependencies