# todo_app
# Phase 3 Full-Stack Todo App

This is a **Full-Stack Todo Application** built with **FastAPI** (backend), **Next.js** (frontend), and **Neon Database**. The app provides a modern, responsive interface for managing tasks securely with authentication.

## Features

- User **Registration** and **Login** with secure JWT authentication.
- **Create, Read, Update, Delete (CRUD)** operations for tasks.
- Tasks are persisted in **Neon DB**.
- Responsive and clean frontend built with **Next.js** and **Tailwind CSS**.
- Protected routes to ensure only authenticated users can access tasks.
- Notifications for success and error events.

## Project Structure

- `backend/` — FastAPI backend with API routes, models, schemas, and services.
- `frontend/` — Next.js frontend with pages, components, and hooks.
- `.claude/` & `.specify/` — AI agent & project specification files.
- `docs/` — Documentation for backend and frontend implementation.

## Getting Started

1. Clone the repository.
2. Follow the backend and frontend setup instructions.
3. Run the app and manage your tasks securely!

## Deployment Instructions

### Backend Deployment
1. Set up your production database (Neon DB or equivalent)
2. Configure environment variables for production:
   - DATABASE_URL: Production database connection string
   - JWT_SECRET_KEY: Strong secret for JWT signing
   - ENVIRONMENT: Set to "production"
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations if applicable
5. Start the server: `uvicorn main:app --host 0.0.0.0 --port 8000`

### Frontend Deployment
1. Set environment variables:
   - NEXT_PUBLIC_API_URL: Base URL for your deployed backend
2. Install dependencies: `npm install` or `yarn install`
3. Build the application: `npm run build` or `yarn build`
4. Start the production server: `npm start` or `yarn start`
5. Alternatively, deploy to Vercel, Netlify, or similar platforms

### Platform-Specific Deployment
#### Deploying to Vercel (Frontend)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push or manually

#### Deploying to Railway/Render (Backend)
1. Connect your GitHub repository
2. Set up environment variables in the platform
3. Configure build and start commands
4. Deploy automatically on push

---

A professional **Todo app** for learning, prototyping, or as a base for full-stack project development.
