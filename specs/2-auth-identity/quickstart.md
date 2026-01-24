# Quickstart Guide: Todo App Authentication Integration

## Overview
This guide explains how to integrate the authentication system into your Todo App, covering both frontend (Better Auth) and backend (JWT verification) components.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Better Auth configured on frontend
- FastAPI backend with JWT verification
- Environment variables set up for authentication

## Environment Setup

### Frontend Environment Variables
Create a `.env.local` file in your frontend directory:
```bash
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-key-here
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### Backend Environment Variables
Create a `.env` file in your backend directory:
```bash
BETTER_AUTH_SECRET=your-super-secret-key-here
DATABASE_URL=postgresql://...
JWT_ALGORITHM=HS256
```

## Frontend Integration Steps

### 1. Install Better Auth
```bash
npm install better-auth
```

### 2. Configure Better Auth Client
Set up the Better Auth client with JWT plugin enabled in your frontend application.

### 3. Implement Authentication Components
- Create login and registration forms
- Implement JWT token storage and retrieval
- Add authentication context provider

### 4. Attach JWT to API Requests
Configure your API service to attach JWT tokens to all protected requests using the Authorization: Bearer header.

## Backend Integration Steps

### 1. Install JWT Dependencies
```bash
pip install python-jose[cryptography] python-multipart
```

### 2. Configure JWT Verification
Set up JWT verification middleware in your FastAPI application to validate tokens against the BETTER_AUTH_SECRET.

### 3. Protect API Routes
Apply JWT verification dependency to all routes that require authentication.

### 4. Extract User Identity
Decode JWT tokens to extract user identity (user_id, email) for authorization decisions.

## Testing the Integration

### 1. Registration Flow
1. Navigate to registration page
2. Enter valid email and password
3. Verify account creation and JWT token receipt

### 2. Login Flow
1. Navigate to login page
2. Enter registered email and password
3. Verify successful authentication and JWT token receipt

### 3. Protected API Access
1. Make authenticated requests to protected endpoints
2. Verify that valid JWT tokens grant access
3. Verify that invalid/missing tokens return 401 Unauthorized

### 4. Token Expiration
1. Test behavior when JWT tokens expire
2. Verify proper error handling and re-authentication requirements

## Security Considerations
- Store JWT secrets securely and never expose them in client-side code
- Use HTTPS in production to prevent token interception
- Implement proper token refresh mechanisms if needed
- Validate JWT signatures on every protected request
- Never trust user identity from client input - always decode from JWT