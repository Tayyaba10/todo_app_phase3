from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings
# Import all models to register them with SQLModel metadata
from ..models.user import User
from ..models.task import Task
from ..models.conversation import Conversation
from ..models.message import Message


# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True to see SQL queries in logs
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    """
    with Session(engine) as session:
        yield session