from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlmodel import SQLModel
from .api.routes import tasks
from .api.routes import auth
from .api.routes import chat
from .core.config import settings
from .core.database import engine
import logging
import traceback
from datetime import datetime


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_error_monitoring(app: FastAPI):
    """
    Set up comprehensive error monitoring for the application.
    """
    @app.middleware("http")
    async def error_monitoring_middleware(request: Request, call_next):
        start_time = datetime.utcnow()
        try:
            response = await call_next(request)
            # Log successful requests
            if response.status_code >= 400:
                logger.warning(f"Request failed: {request.method} {request.url} - Status: {response.status_code}")
            return response
        except Exception as e:
            # Log the error with full context
            process_time = (datetime.utcnow() - start_time).total_seconds()
            logger.error(
                f"Unhandled exception in {request.method} {request.url.path} "
                f"Query: {request.query_params} "
                f"Headers: {dict(request.headers)} "
                f"Process time: {process_time}s "
                f"Error: {str(e)} "
                f"Traceback: {traceback.format_exc()}"
            )
            # Re-raise the exception to be handled by FastAPI's exception handlers
            raise
        finally:
            # Log request metrics
            process_time = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"{request.method} {request.url.path} - {response.status_code if 'response' in locals() else 'ERR'} - {process_time:.3f}s")


# Global exception handler
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc} at {request.url}", exc_info=True)
    return {"detail": "Internal server error", "error_id": str(exc.__hash__())}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create all database tables
    logger.info("Creating database tables...")
    try:
        # Create all tables with the new schema
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully with new schema")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    yield
    # Shutdown: Cleanup can go here if needed
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Todo App Backend API",
        description="Secure, JWT-authenticated backend API for task management",
        version="1.0.0",
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        # Expose the authorization header to client-side applications
        #expose_headers=["Access-Control-Allow-Origin", "Authorization"]
    )

    # Add rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Set up comprehensive error monitoring
    setup_error_monitoring(app)

    # Include API routes
    app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(chat.router, prefix="/api", tags=["chat"])

    @app.get("/")
    def read_root():
        return {"message": "Todo App Backend API", "version": "1.0.0"}

    return app


# Create the application instance
app = create_app()