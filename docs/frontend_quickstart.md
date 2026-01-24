# Frontend Quickstart Guide

## Getting Started

This guide will help you quickly set up and run the Todo App frontend.

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file in the frontend root directory with the following content:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   ```

## Running the Application

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Open your browser and navigate to `http://localhost:3000`

## Key Features to Test

### User Registration and Login
1. Click on "Sign Up" in the header
2. Fill in the registration form with valid email and password
3. Verify successful registration and redirect to dashboard
4. Log out and log back in to verify login functionality

### Task Management
1. After logging in, navigate to "My Tasks" or "Dashboard"
2. Create a new task using the "Create Task" button
3. Verify the task appears in the task list
4. Toggle task completion status
5. Edit an existing task
6. Delete a task

### Authentication Protection
1. Try navigating directly to `/tasks` when not logged in
2. Verify automatic redirect to login page
3. After logging in, verify return to intended page

## Expected Behavior

- All forms should have proper validation
- Error messages should be displayed appropriately
- Successful actions should trigger notifications
- Protected routes should redirect unauthenticated users
- Session should be maintained across page refreshes
- Automatic logout when token expires

## Troubleshooting

- If authentication issues occur, clear browser storage and log in again
- Check browser console for any JavaScript errors
- Verify the backend API is running and accessible at the configured URL