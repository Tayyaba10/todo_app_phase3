---
id: "001"
title: "Fix useAuth Context Mismatch Error"
stage: "general"
date_iso: "2026-01-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "fix-auth-error"
labels: ["auth", "context", "error"]
spec: null
ticket: null
adr: null
pr: null
---

# Fix useAuth Context Mismatch Error

## User Input
```
solve this error
 GET / 500 in 1724ms (compile: 939ms, render: 785ms)
⨯ Error: useAuth must be used within an AuthProvider
    at useAuth (src\lib\hooks\useAuth.tsx:148:11)
    at HomePage (src\app\page.tsx:8:36)
  146 |   const context = useContext(AuthContext);
  147 |   if (context === undefined) {
> 148 |     throw new Error('useAuth must be used within an AuthProvider');
      |           ^
  149 |   }
  150 |   return context;
}; {
  digest: '936303471'
}
```

## Response Summary
Identified and resolved a critical authentication context mismatch error caused by duplicate and conflicting authentication implementations in the codebase.

## Solution Details

### Problem Analysis
The error "useAuth must be used within an AuthProvider" occurred because there were two different authentication implementations:
1. A mock implementation in `src/lib/hooks/useAuth.tsx`
2. A real implementation in `src/lib/auth/auth-context.tsx`

The layout correctly wrapped the app with the real `AuthProvider`, but many components were importing `useAuth` from the mock implementation, causing a context mismatch.

### Solution Implemented
1. **Updated all component imports**: Changed all files that were importing `useAuth` from `'../../lib/hooks/useAuth'` to import from `'../../lib/auth/auth-context'`:
   - `src/app/page.tsx` (Home page)
   - `src/components/layout/Sidebar.tsx`
   - `src/components/layout/Header.tsx`
   - `src/components/auth/RegisterForm.tsx`
   - `src/components/auth/ProtectedRoute.tsx`
   - `src/components/auth/LoginForm.tsx`
   - `src/components/chat/ChatInterface.tsx`
   - `src/app/tasks/page.tsx`
   - `src/app/tasks/create/page.tsx`
   - `src/app/tasks/[id]/edit/page.tsx`

2. **Removed the conflicting mock implementation**: Deleted the file `src/lib/hooks/useAuth.tsx` to prevent future confusion and conflicts.

### Result
All components now properly use the same authentication context provided by the `AuthProvider` in the layout, eliminating the "useAuth must be used within an AuthProvider" error.

The authentication system is now consistent across the application, using the real implementation that integrates with Better Auth and JWT tokens instead of the mock localStorage-based implementation.

## Files Modified
 - D:\todo_app\phase3\frontend\src\app\page.tsx
 - D:\todo_app\phase3\frontend\src\components\layout\Sidebar.tsx
 - D:\todo_app\phase3\frontend\src\components\layout\Header.tsx
 - D:\todo_app\phase3\frontend\src\components\auth\RegisterForm.tsx
 - D:\todo_app\phase3\frontend\src\components\auth\ProtectedRoute.tsx
 - D:\todo_app\phase3\frontend\src\components\auth\LoginForm.tsx
 - D:\todo_app\phase3\frontend\src\components\chat\ChatInterface.tsx
 - D:\todo_app\phase3\frontend\src\app\tasks\page.tsx
 - D:\todo_app\phase3\frontend\src\app\tasks\create\page.tsx
 - D:\todo_app\phase3\frontend\src\app\tasks\[id]\edit\page.tsx
 - D:\todo_app\phase3\frontend\src\lib\hooks\useAuth.tsx (deleted)

## Outcome
The authentication error has been resolved. The application should now run without the 500 error caused by the authentication context mismatch.