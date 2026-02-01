---
id: "002"
title: "Fix API Endpoint Mismatches and Network Errors"
stage: "general"
date_iso: "2026-01-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "fix-api-endpoints"
labels: ["api", "network", "endpoints", "backend"]
spec: null
ticket: null
adr: null
pr: null
---

# Fix API Endpoint Mismatches and Network Errors

## User Input
```
Console TypeError

Failed to fetch
src/components/auth/LoginForm.tsx (25:13) @ handleSubmit

  23 |
  24 |     try {
> 25 |       await login(email, password);
     |             ^
  26 |
  27 |       // Call success callback if provided
  28 |       if (onSuccess) {
```

## Response Summary
Identified and resolved multiple API endpoint mismatches between frontend and backend that were causing "Failed to fetch" errors.

## Solution Details

### Problem Analysis
The error was caused by multiple API endpoint mismatches between the frontend and backend:
1. Auth endpoints had duplicated path segments (/api/auth/auth/login instead of /api/auth/login)
2. Task endpoints had inconsistent path structures (/tasks/api/tasks/{id} instead of /tasks/{id})
3. Duplicate API base URLs in environment file
4. Backend server potentially not running on expected port

### Solution Implemented
1. **Fixed backend auth routes** to remove duplicated path segments:
   - Changed @router.post("/auth/login") to @router.post("/login")
   - Changed @router.get("/auth/profile") to @router.get("/profile")

2. **Fixed backend task routes** to remove duplicated path segments:
   - Changed @router.get("/api/tasks/{task_id}") to @router.get("/{task_id}")
   - Changed @router.put("/api/tasks/{task_id}") to @router.put("/{task_id}")
   - Changed @router.delete("/api/tasks/{task_id}") to @router.delete("/{task_id}")
   - Changed @router.patch("/api/tasks/{task_id}/complete") to @router.patch("/{task_id}/complete")

3. **Updated frontend API service** to match corrected backend endpoints:
   - Updated login endpoint from '/api/auth/auth/login' to '/api/auth/login'
   - Updated profile endpoint from '/api/auth/auth/profile' to '/api/auth/profile'
   - Updated task endpoints to use correct paths without duplicated segments

4. **Cleaned up environment variables** by removing duplicate NEXT_PUBLIC_API_BASE_URL

### Result
All API endpoints now correctly match between frontend and backend, resolving the "Failed to fetch" network errors. The authentication and task management functionality should now work correctly.

## Files Modified
 - D:\todo_app\phase3\backend\src\api\routes\auth.py
 - D:\todo_app\phase3\backend\src\api\routes\tasks.py
 - D:\todo_app\phase3\frontend\src\lib\services\api.ts
 - D:\todo_app\phase3\frontend\.env.local

## Outcome
The login functionality and other API calls should now work without network errors, assuming the backend server is running on the expected port (127.0.0.1:8000).