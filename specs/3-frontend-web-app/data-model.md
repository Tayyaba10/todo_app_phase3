# Data Model: Frontend State and UI Components

## User Session State

### Properties
- **isAuthenticated**: Boolean indicating authentication status
- **user**: Object containing user information (id, email, name)
- **token**: JWT token string for API authentication
- **isLoading**: Boolean indicating auth state loading
- **error**: Error message if auth operation fails

### Transitions
- Unauthenticated → Loading → Authenticated (successful login/register)
- Unauthenticated → Loading → Error (failed login/register)
- Authenticated → Loading → Unauthenticated (logout)

## Task State

### Properties
- **id**: Unique identifier for the task
- **title**: Task title string
- **description**: Optional task description
- **completed**: Boolean indicating completion status
- **createdAt**: Timestamp of creation
- **updatedAt**: Timestamp of last update
- **userId**: Owner of the task (matches authenticated user)

### Operations
- **CREATE**: Add new task to user's task list
- **READ**: Fetch user's tasks from backend
- **UPDATE**: Modify existing task properties
- **DELETE**: Remove task from user's list

## UI Component States

### TaskList Component
- **tasks**: Array of task objects
- **loading**: Boolean indicating fetch status
- **error**: Error message if fetch fails
- **empty**: Boolean indicating no tasks exist

### TaskForm Component
- **formData**: Object containing form inputs
- **submitting**: Boolean indicating submission status
- **error**: Error message if submission fails
- **success**: Success message after submission

### AuthForm Component
- **formData**: Object containing email/password
- **submitting**: Boolean indicating submission status
- **error**: Error message if submission fails
- **success**: Success message after submission

## API Response States

### Loading States
- **idle**: Initial state before request
- **loading**: Request in progress
- **success**: Request completed successfully
- **error**: Request failed

### Error States
- **networkError**: Connection issues
- **validationError**: Client-side validation issues
- **authError**: Authentication/authorization issues
- **serverError**: Server-side processing issues

## Navigation State

### Route Protection
- **publicRoutes**: Array of routes accessible without authentication
- **protectedRoutes**: Array of routes requiring authentication
- **redirectPath**: Path to redirect after authentication