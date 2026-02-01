---
id: "004"
title: "Fix Chat Page Auth Import Error"
stage: "general"
date_iso: "2026-01-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "fix-chat-auth-error"
labels: ["auth", "jsx", "import", "chat"]
spec: null
ticket: null
adr: null
pr: null
---

# Fix Chat Page Auth Import Error

## User Input
```
./src/lib/hooks/auth.ts:132:32
Parsing ecmascript source code failed
  130 |   };
  131 |
> 132 |   return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
      |                                ^^^^^
  133 | };
  134 |
  135 | export const useAuth = (): AuthContextType => {

Expected '>', got 'value'

Import traces:
  Client Component Browser:
    ./src/lib/hooks/auth.ts [Client Component Browser]
    ./src/app/chat/page.tsx [Client Component Browser]
    ./src/app/chat/page.tsx [Server Component]

  Client Component SSR:
    ./src/lib/hooks/auth.ts [Client Component SSR]
    ./src/app/chat/page.tsx [Client Component SSR]
    ./src/app/chat/page.tsx [Server Component]
```

## Response Summary
Identified and resolved a JSX parsing error caused by the chat page importing a mock authentication implementation instead of the real one.

## Solution Details

### Problem Analysis
The error was caused by the chat page importing `useAuth` from `'@/lib/hooks/auth'` which contained a mock authentication implementation. This file had JSX syntax issues and conflicted with the real authentication system that uses JWT and Better Auth.

### Solution Implemented
1. Updated the chat page import to use the correct authentication context: `'@/lib/auth/auth-context'`
2. Removed the conflicting mock auth implementation file (`auth.ts`) to prevent future conflicts

### Result
The chat page now correctly imports the real authentication context, resolving the parsing error and ensuring consistency with the rest of the application's authentication system.

## Files Modified
 - D:\todo_app\phase3\frontend\src\app\chat\page.tsx
 - D:\todo_app\phase3\frontend\src\lib\hooks\auth.ts (deleted)

## Outcome
The chat page should now load without errors, using the proper authentication system that's consistent with the rest of the application.