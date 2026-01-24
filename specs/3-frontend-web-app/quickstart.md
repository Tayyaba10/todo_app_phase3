# Quickstart Guide: Todo App Frontend Integration

## Overview
This guide explains how to set up and run the frontend application that connects to the Todo App backend services.

## Prerequisites
- Node.js 18+ installed
- The backend service is running and accessible
- Environment variables configured for API endpoints

## Setup Instructions

### 1. Clone and Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment Variables
Copy the example environment file and update with your configuration:
```bash
cp .env.example .env.local
```

Update the following variables:
- `NEXT_PUBLIC_API_BASE_URL`: URL of your backend API (e.g., http://localhost:8000)
- `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for Better Auth (e.g., http://localhost:3000)

### 3. Run the Development Server
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Key Features

### Authentication Flow
1. Users can register/login via the Better Auth UI
2. JWT tokens are automatically attached to all protected API requests
3. Unauthorized users are redirected to the login page

### Task Management
1. Authenticated users can create new tasks
2. Users can view, edit, and delete their own tasks
3. Task completion status can be toggled

### State Management
- Authentication state is managed via AuthContext
- API requests are handled through centralized service
- Loading, error, and empty states are properly handled

## API Integration

### Protected Endpoints
All task-related endpoints require authentication:
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `PATCH /api/tasks/:id/complete` - Toggle completion

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

## Testing the Integration
1. Visit http://localhost:3000
2. Register a new account or log in with existing credentials
3. Verify that you can create, view, edit, and delete tasks
4. Check that unauthorized access redirects to login
5. Verify that JWT tokens are being properly attached to API requests