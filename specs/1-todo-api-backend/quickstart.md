# Quickstart: Todo App Backend API

## Prerequisites
- Python 3.11+
- Neon PostgreSQL account
- Better Auth configured for frontend

## Environment Setup
1. Create `.env` file with the following variables:
```
DATABASE_URL=postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname
BETTER_AUTH_SECRET=your_better_auth_secret
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application
1. Start the backend server:
```bash
uvicorn backend.src.main:app --reload
```

2. The API will be available at `http://localhost:8000/api`

## Testing the API
1. Obtain a JWT token from your Better Auth frontend
2. Make authenticated requests with the header:
```
Authorization: Bearer <your_jwt_token>
```

## Available Endpoints
- GET /api/tasks - List user's tasks
- POST /api/tasks - Create new task
- GET /api/tasks/{id} - Get specific task
- PUT /api/tasks/{id} - Update task
- DELETE /api/tasks/{id} - Delete task
- PATCH /api/tasks/{id}/complete - Toggle task completion