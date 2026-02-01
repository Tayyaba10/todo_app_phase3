---
id: 001
title: Fix chat API route undefined userId issue
stage: general
date_iso: 2026-01-29
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: claude
command: fix-chat-api-issue
labels: ["bug-fix", "api", "chat", "routing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - D:\todo_app\phase3\frontend\src\lib\services\api.ts
  - D:\todo_app\phase3\frontend\src\components\chat\ChatInterface.tsx
tests_yaml: []
---

# Fix chat API route undefined userId issue

## Summary
Fixed an issue where the chat API was returning a 422 error with the route `/api/undefined/chat` instead of the correct route with the user ID.

## Root Cause
The issue was caused by two problems in the frontend API service:
1. The base URL included `/api` which caused double-prefixing when combined with individual API endpoints
2. The ChatInterface component was using an undefined `apiClient` instead of the proper `apiService`

## Changes Made
1. Updated the API service base URL to not include `/api` (changed from `http://127.0.0.1:8000/api` to `http://127.0.0.1:8000`)
2. Updated all API endpoints to include the `/api` prefix explicitly (e.g., `/tasks/` became `/api/tasks/`)
3. Fixed the ChatInterface component to use `apiService.sendMessage()` instead of undefined `apiClient.post()`
4. Updated the ChatInterface import from `apiClient` to `apiService`

## Result
The chat API now properly constructs URLs like `/api/{userId}/chat` instead of `/api/undefined/chat`, resolving the 422 Unprocessable Entity error.

## Files Modified
- frontend/src/lib/services/api.ts
- frontend/src/components/chat/ChatInterface.tsx