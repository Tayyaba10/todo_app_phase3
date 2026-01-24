# Todo App Backend API

This is the backend API for the Todo App, providing secure, JWT-authenticated task management functionality.

## Features

- Secure JWT-based authentication
- Full CRUD operations for tasks
- User-level data isolation (users can only access their own tasks)
- RESTful API design
- Input validation and error handling

## Tech Stack

- **Framework**: FastAPI
- **Database ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT tokens
- **Dependencies**: See `requirements.txt`

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Copy `.env.example` to `.env` and fill in the required values:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. Start the development server:
   ```bash
   uvicorn backend.src.main:app --reload
   ```

## API Endpoints

All API endpoints are documented in `docs/backend_api.md`.

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string
- `JWT_SECRET_KEY`: Secret key for signing JWT tokens
- `BETTER_AUTH_SECRET`: Better Auth secret (for frontend integration)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

## Testing

Run the unit tests:
```bash
pytest tests/unit/
```

Run all tests:
```bash
pytest
```

## Security

- All endpoints require JWT authentication
- Users can only access and modify their own tasks
- Input validation is performed on all requests
- SQL injection protection through SQLModel/SQLAlchemy

## Project Structure

```
backend/
├── src/
│   ├── models/          # Database models
│   ├── services/        # Business logic
│   ├── api/
│   │   ├── routes/      # API endpoints
│   │   └── schemas/     # Request/response schemas
│   ├── core/            # Core configurations
│   └── utils/           # Utility functions
├── tests/               # Test files
├── requirements.txt     # Dependencies
└── .env.example         # Environment variables template
```